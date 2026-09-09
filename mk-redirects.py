#!/usr/bin/env python3
"""Writes the App Store redirect pages: /, /download, /ig, /tt, /yt.

Each page (1) logs one click to Supabase `link_clicks` (anon insert-only,
see supabase/migrations 'link_clicks'), then (2) sends the visitor to the
App Store with an Apple campaign tag, ct=<source>. App Store Connect →
App Analytics → Sources → Campaigns then reports page views / installs /
proceeds per source. Click → install rate = installs(ct) / clicks(source).

Source per page:
  /ig /tt /yt      fixed (ig_bio / tt_bio / yt)
  /  /download     ?s=<tag> if given, else by referrer (instagram → ig_bio,
                   tiktok → tt_bio, youtube → yt, x/twitter → x), else direct.

PT = Apple provider token (App Store Connect → App Analytics → Sources →
Campaigns → Generate Campaign Link shows it as pt=…). Empty = the ct tag
still goes out but Apple will not attribute it. Run: python3 mk-redirects.py
"""
import os

APP_ID = "6802901402"
PT = "128667679"  # Apple provider token (ASC olympus session providerId, 2026-09-09)
SUPABASE_URL = "https://bvaumyrtcuehlipiaxlv.supabase.co"
SUPABASE_KEY = "sb_publishable_WwcAtQ0r_O-YyxFM97ciKg_eRIaQxe7"  # publishable, insert-only via RLS

PAGES = {  # path → fixed source ('' = detect)
    "index.html": "",
    "download/index.html": "",
    "ig/index.html": "ig_bio",
    "tt/index.html": "tt_bio",
    "yt/index.html": "yt",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>
(function(){{
  var fixed={fixed!r},pt={pt!r},base="https://apps.apple.com/app/apple-store/id{app_id}";
  var ref=document.referrer||"",q=new URLSearchParams(location.search).get("s")||"";
  var src=fixed||(q&&/^[a-z0-9_-]{{1,40}}$/i.test(q)?q:"")||
    (/instagram\\.com/i.test(ref)?"ig_bio":/tiktok\\.com/i.test(ref)?"tt_bio":
     /youtube\\.com|youtu\\.be/i.test(ref)?"yt":/twitter\\.com|x\\.com|t\\.co/i.test(ref)?"x":"direct");
  var url=base+"?"+(pt?"pt="+pt+"&":"")+"ct="+src+"&mt=8";
  try{{
    fetch({sb_url!r}+"/rest/v1/link_clicks",{{method:"POST",keepalive:true,
      headers:{{"apikey":{sb_key!r},"Authorization":"Bearer "+{sb_key!r},
        "Content-Type":"application/json","Prefer":"return=minimal"}},
      body:JSON.stringify({{source:src,path:location.pathname,referrer:ref.slice(0,500),
        ua:navigator.userAgent.slice(0,500),lang:navigator.language}})}});
  }}catch(e){{}}
  location.replace(url);
}})();
</script>
<meta http-equiv="refresh" content="0;url={plain}">
<title>Meal Pic on the App Store</title>
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="canonical" href="https://apps.apple.com/app/id{app_id}">
<link rel="icon" href="data:,">
<style>body{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;background:#fff;color:#111;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0}}p{{font-size:17px}}a{{color:#0a84ff}}</style>
</head>
<body>
<p><a href="{plain}">Meal Pic on the App Store</a></p>
</body>
</html>
"""

here = os.path.dirname(os.path.abspath(__file__))
for path, fixed in PAGES.items():
    ct = fixed or "direct"
    plain = f"https://apps.apple.com/app/apple-store/id{APP_ID}?" + (f"pt={PT}&" if PT else "") + f"ct={ct}&mt=8"
    out = os.path.join(here, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        f.write(TEMPLATE.format(fixed=fixed, pt=PT, app_id=APP_ID, sb_url=SUPABASE_URL, sb_key=SUPABASE_KEY, plain=plain))
    print("wrote", path, "→ ct =", ct if fixed else "detect")
