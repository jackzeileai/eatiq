# Coarse link geography

Cloudflare Worker reads only country and US regionCode from trusted request.cf metadata.
No IP, city, coordinates, cookies, or account IDs are stored by this collector. GPC/DNT
suppresses geography. User-Agent is retained for the existing bot exclusion.
Request logging/observability is disabled. The browser redirects immediately and sends
one keepalive request; failures never block App Store navigation and are not retried.

Deploy: `wrangler deploy --config click-worker/wrangler.toml`.
Requires Meal Pic migration `0022_click_locations.sql` first. Public Supabase key is
insert-only under RLS; no service-role secret is shipped. Endpoint is
https://mealpic-clicks.jackzeile.workers.dev.

Old clicks have NULL location. Apple downloads remain country-level. Geography is
approximate and VPNs/relays may reflect the exit region rather than the visitor.
