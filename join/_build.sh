#!/bin/sh
# Builds both creator landing pages from _src.html: /join (app look) and /join/v2 (Partiful look).
cd "$(dirname "$0")"
sed -e 's/__THEME__/app/' -e 's#__ROOT__#../#g' _src.html > index.html
sed -e 's/__THEME__/party/' -e 's#__ROOT__#../../#g' _src.html > v2/index.html
