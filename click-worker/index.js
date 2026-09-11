// Geography comes only from Cloudflare, never browser-supplied location fields.
const ORIGINS = new Set(["https://mealpic.app", "https://www.mealpic.app"]);
const API = "https://bvaumyrtcuehlipiaxlv.supabase.co/rest/v1/link_clicks";
const KEY = "sb_publishable_WwcAtQ0r_O-YyxFM97ciKg_eRIaQxe7"; // public, insert-only
export default {
  async fetch(request) {
    const origin = request.headers.get("Origin");
    const headers = { "Access-Control-Allow-Origin": origin || "https://mealpic.app", "Vary": "Origin", "Cache-Control": "no-store" };
    if (!ORIGINS.has(origin)) return new Response(null, { status: 403 });
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: { ...headers, "Access-Control-Allow-Methods": "POST", "Access-Control-Allow-Headers": "Content-Type" } });
    if (request.method !== "POST") return new Response(null, { status: 405, headers });
    if (Number(request.headers.get("Content-Length")) > 2048) return new Response(null, { status: 413, headers });
    let body;
    try { const text = await request.text(); if (text.length > 2048) throw new Error(); body = JSON.parse(text); } catch { return new Response(null, { status: 400, headers }); }
    if (!body || !/^[a-z0-9_-]{1,40}$/i.test(body.source || "") || typeof body.path !== "string" || body.path.length > 200) return new Response(null, { status: 400, headers });
    const optOut = body.privacyOptOut === true || request.headers.get("Sec-GPC") === "1" || request.headers.get("DNT") === "1";
    const cf = request.cf || {};
    const country = !optOut && /^[A-Z]{2}$/.test(cf.country || "") && !["XX", "T1"].includes(cf.country) ? cf.country : null;
    const region = country === "US" && /^[A-Z]{2}$/.test(cf.regionCode || "") ? cf.regionCode : null;
    // IP and full request headers are never forwarded, persisted, or logged.
    const row = { source: body.source, path: body.path, ua: (request.headers.get("User-Agent") || "").slice(0,500), country, region };
    try {
      const result = await fetch(API, { method: "POST", headers: { "apikey": KEY, "Authorization": "Bearer " + KEY, "Content-Type": "application/json", "Prefer": "return=minimal" }, body: JSON.stringify(row), signal: AbortSignal.timeout(5000) });
      return new Response(null, { status: result.ok ? 204 : 502, headers });
    } catch { return new Response(null, { status: 502, headers }); }
  }
};
