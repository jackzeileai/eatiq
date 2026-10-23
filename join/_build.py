#!/usr/bin/env python3
"""Builds the creator landing pages from _src.html.
  /join        app look, standard deal (50% of revenue + retainer + cut of ad spend)
  /join/v2     Partiful look, standard deal
  /join/100    app look, the 100%-of-revenue deal (TikTok Shop affiliate ads land here; 2026-10-22)
Deal-only markup sits between <!--deal:50--> … <!--/deal--> (or deal:100); the other deal's blocks are cut."""
import re, pathlib
HERE = pathlib.Path(__file__).parent
SRC = (HERE / "_src.html").read_text()
APP_TC = '<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">'
PARTY_TC = '<meta name="theme-color" content="#0B0B0D">'
DEALS = {
    "50":  {"__PCT__": "50",  "__CUT__": ".5", "__DEAL__": "standard", "__PATH__": "/join/",     "__PAGE__": "join"},
    "100": {"__PCT__": "100", "__CUT__": "1",  "__DEAL__": "rev100",   "__PATH__": "/join/100/", "__PAGE__": "join100"},
}
def build(out, theme, root, deal):
    s = SRC.replace("__THEME__", theme).replace("__ROOT__", root).replace("__THEME_COLOR__", APP_TC if theme == "app" else PARTY_TC)
    for k, v in DEALS[deal].items():
        s = s.replace(k, v)
    other = "100" if deal == "50" else "50"
    s = re.sub(rf"<!--deal:{other}-->.*?<!--/deal-->\n?", "", s, flags=re.S)       # the other deal's blocks go
    s = re.sub(rf"<!--deal:{deal}-->\n|<!--deal:{deal}-->|<!--/deal-->", "", s)     # our markers go, content stays
    assert "__" not in re.sub(r"__(creatorEmail|proto__)", "", s) or not re.search(r"__[A-Z_]+__", s), re.search(r"__[A-Z_]+__", s)
    (HERE / out).parent.mkdir(parents=True, exist_ok=True)
    (HERE / out).write_text(s)
    print(out, len(s))
build("index.html", "app", "../", "50")
build("v2/index.html", "party", "../../", "50")
build("100/index.html", "app", "../../", "100")
