#!/bin/sh
# Builds both creator landing pages from _src.html: /join (app look) and /join/v2 (Partiful look).
cd "$(dirname "$0")"
APP_TC='<meta name="theme-color" content="#FFFFFF">'
PARTY_TC='<meta name="theme-color" content="#0B0B0D">'
sed -e 's/__THEME__/app/' -e 's#__ROOT__#../#g' -e "s|__THEME_COLOR__|$APP_TC|" _src.html > index.html
sed -e 's/__THEME__/party/' -e 's#__ROOT__#../../#g' -e "s|__THEME_COLOR__|$PARTY_TC|" _src.html > v2/index.html
