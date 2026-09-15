// mealpic.app edge redirect (2026-09-14). Sits in front of the GitHub Pages
// site once the zone is on Cloudflare. For the App Store paths it logs the
// click server-side (before anything else can happen) and answers with a 302
// to the App Store campaign link — no page, no script, so the Instagram
// in-app browser hands off in one hop. Every other path is passed through to
// GitHub Pages untouched. If this worker is ever down, Cloudflare serves the
// origin and the old script-based redirect pages still work.
//
// Same rules as website/mk-redirects.py and click-worker/index.js:
//   /ig /tt /yt /fb = fixed source (/fb = Meta/Facebook/Instagram paid ads); / and /download = ?s= tag, else referrer host
//   (instagram → ig_bio, tiktok → tt_bio, youtube → yt, x → x, mealpic → site,
//   other → direct), NO referrer → ig_bio (the bio link is the bare domain).
// Geography = Cloudflare's country + US region only; GPC/DNT suppresses it.
// asn_org = who owns the visitor's network — link_clicks_real drops hosting
// companies (Microsoft/Amazon/Google clouds = the security scanners that
// messaging and email apps run on links).
const APP_ID = "6802901402", PT = "128667679";
const API = "https://bvaumyrtcuehlipiaxlv.supabase.co/rest/v1/link_clicks";
const KEY = "sb_publishable_WwcAtQ0r_O-YyxFM97ciKg_eRIaQxe7"; // public, insert-only under RLS
const FIXED = { "/ig": "ig_bio", "/tt": "tt_bio", "/yt": "yt", "/fb": "meta_ads", "/": "", "/download": "" };
const STORE_PAGE = `https://apps.apple.com/us/app/id${APP_ID}`;

function sourceFor(path, url, referrer) {
  if (FIXED[path]) return FIXED[path];
  const s = url.searchParams.get("s") || "";
  if (/^[a-z0-9_-]{1,40}$/i.test(s)) return s;
  const ref = referrer || "";
  if (/instagram\.com/i.test(ref)) return "ig_bio";
  if (/tiktok\.com/i.test(ref)) return "tt_bio";
  if (/youtube\.com|youtu\.be/i.test(ref)) return "yt";
  if (/twitter\.com|x\.com|t\.co/i.test(ref)) return "x";
  if (/mealpic\.app/i.test(ref)) return "site";
  return ref ? "direct" : "ig_bio";
}

function logClick(request, path, source) {
  const h = request.headers, cf = request.cf || {};
  const optOut = h.get("Sec-GPC") === "1" || h.get("DNT") === "1";
  const country = !optOut && /^[A-Z]{2}$/.test(cf.country || "") && !["XX", "T1"].includes(cf.country) ? cf.country : null;
  const region = country === "US" && /^[A-Z]{2}$/.test(cf.regionCode || "") ? cf.regionCode : null;
  const refHost = ((h.get("Referer") || "").match(/^https?:\/\/([^\/:?#]+)/i) || [])[1] || null;
  const row = {
    source, path, ua: (h.get("User-Agent") || "").slice(0, 500),
    referrer: refHost && /^[a-z0-9.-]{1,120}$/i.test(refHost) ? refHost.toLowerCase() : null,
    country, region, asn_org: (cf.asOrganization || "").slice(0, 120) || null,
  };
  return fetch(API, {
    method: "POST", signal: AbortSignal.timeout(5000),
    headers: { apikey: KEY, Authorization: "Bearer " + KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
    body: JSON.stringify(row),
  }).catch(() => {});
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    let path = url.pathname.replace(/\/index\.html$/, "").replace(/\/+$/, "") || "/";
    if (!(path in FIXED) || (request.method !== "GET" && request.method !== "HEAD")) return fetch(request);
    const ua = request.headers.get("User-Agent") || "";
    // Link previewers (iMessage, WhatsApp, Instagram DMs, Slack…) get the real
    // page so the preview shows "Meal Pic on the App Store"; not a click.
    if (/bot|crawl|spider|preview|facebookexternalhit|facebot|whatsapp|telegram|slack|discord|linkedin|pinterest|snapchat/i.test(ua)) return fetch(request);
    const source = sourceFor(path, url, request.headers.get("Referer"));
    ctx.waitUntil(logClick(request, path, source));
    const store = `https://apps.apple.com/app/apple-store/id${APP_ID}?pt=${PT}&ct=${encodeURIComponent(source)}&mt=8`;
    return new Response(null, { status: 302, headers: { Location: store, "Cache-Control": "no-store", "Referrer-Policy": "no-referrer" } });
  },
};
