# mealpic.app edge redirect

Cloudflare Worker that answers `/`, `/ig`, `/tt`, `/yt`, `/download` with a 302
straight to the App Store campaign link (pt + ct), logging the click to Supabase
`link_clicks` first (with country, US region, referrer host, network owner).
Every other path passes through to GitHub Pages. If the worker is down, the old
script-based redirect pages on GitHub Pages still work.

Deploy: `wrangler deploy --config redirect-worker/wrangler.toml`.
Test URL: https://mealpic-redirect.jackzeile.workers.dev/ig

Going live on the real domain needs the zone on Cloudflare:
1. Cloudflare → Add a site → mealpic.app (Free). Records that must exist
   (all verified by dig 2026-09-14): A @ 185.199.108/109/110/111.153 (proxied),
   CNAME www → jackzeileai.github.io (proxied), MX @ 10 mxa/mxb.mailgun.org,
   TXT @ "v=spf1 include:mailgun.org ~all", TXT _dmarc (DMARC1 p=none…),
   TXT resend._domainkey (p=MIGf…), MX send 10 feedback-smtp.us-east-1.amazonses.com,
   TXT send "v=spf1 include:amazonses.com ~all". SSL/TLS mode: Full (strict).
2. Uncomment `routes` in wrangler.toml and redeploy.
3. Squarespace Domains → mealpic.app → nameservers → Cloudflare's pair.
4. After propagation: `curl -I https://mealpic.app/ig` must be a 302 to apps.apple.com.
