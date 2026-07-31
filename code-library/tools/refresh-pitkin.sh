#!/bin/bash
set -u
OUT=/home/user/drawing-set/code-library/pitkin
PDF=/tmp/claude-0/-home-user-drawing-set/031e023b-add5-5506-be7d-63e1feca92b0/scratchpad/pitkin-pdf
mkdir -p "$OUT" "$PDF"
UA="Mozilla/5.0 (X11; Linux x86_64)"

grab () {  # name url
  local name="$1" url="$2"
  echo "== $name"
  curl -sS -L --cacert /root/.ccr/ca-bundle.crt -A "$UA" -o "$PDF/$name.pdf" "$url" || { echo "DL FAIL $name"; return 1; }
  file "$PDF/$name.pdf" | grep -qi pdf || { echo "NOT PDF: $name"; head -c 200 "$PDF/$name.pdf"; echo; return 1; }
  pdftotext -layout "$PDF/$name.pdf" "$OUT/$name.txt" || { echo "EXTRACT FAIL $name"; return 1; }
  echo "$name ok: $(du -h "$PDF/$name.pdf" | cut -f1) pdf, $(wc -l < "$OUT/$name.txt") lines"
}

grab home-rule-charter                       "https://pitkincounty.com/DocumentCenter/View/33674/11-05-2024_hrc"
grab title-02-administration-personnel       "https://pitkincounty.com/DocumentCenter/View/35504/title-02-administration-and-personnel"
grab title-03-revenue-finance                "https://pitkincounty.com/DocumentCenter/View/35505/title-03-revenue-and-finance-3-8"
grab title-04-campaign-contributions         "https://www.pitkincounty.com/DocumentCenter/View/33195/title-04-campaign-contributions-and-expenditures-_ord013-2012"
grab title-05-animals                        "https://www.pitkincounty.com/DocumentCenter/View/32181/Title-5---Animals-1"
grab title-06-health-safety                  "https://pitkincounty.com/DocumentCenter/View/35900/Title-6---Health-and--Safety-2"
grab title-07-public-peace-welfare           "https://www.pitkincounty.com/DocumentCenter/View/33197/title-07-public-peace-and-welfare"
grab title-09-roads-public-places            "https://pitkincounty.com/DocumentCenter/View/35759/Title-9---Roads-and-Public-Places"
grab title-10-airport-regulations            "https://pitkincounty.com/DocumentCenter/View/36163/260325-Title-10---Airport-Regulations-se-582026"
grab title-11-building-construction          "https://pitkincounty.com/DocumentCenter/View/36414/Title-11-Buildings-and-Construction"
grab title-12-open-space-trails              "https://www.pitkincounty.com/DocumentCenter/View/32186/title-12---Open-Space-and-Trails-1"
grab luc-ch01-general-provisions             "https://pitkincounty.com/DocumentCenter/View/36161/chapter-01"
grab luc-ch02-review-approval-procedures     "https://pitkincounty.com/DocumentCenter/View/34573/chapter-02"
grab luc-ch03-zoning-districts               "https://pitkincounty.com/DocumentCenter/View/36305/chapter-03"
grab luc-ch04-permitted-uses                 "https://pitkincounty.com/DocumentCenter/View/35644/chapter-04"
grab luc-ch05-dimensional-requirements       "https://pitkincounty.com/DocumentCenter/View/35921/chapter-05"
grab luc-ch06-growth-management-tdrs         "https://pitkincounty.com/DocumentCenter/View/36078/chapter-06"
grab luc-ch07-development-standards          "https://pitkincounty.com/DocumentCenter/View/36079/chapter-07"
grab luc-ch08-exactions-impact-fees          "https://pitkincounty.com/DocumentCenter/View/35424/chapter-08"
grab luc-ch09-non-conformities               "https://pitkincounty.com/DocumentCenter/View/36080/chapter-09"
grab luc-ch10-violations-enforcement         "https://www.pitkincounty.com/DocumentCenter/View/32183/Title-8-Chapter-10---LUC-1"
grab luc-ch11-definitions                    "https://pitkincounty.com/DocumentCenter/View/36081/chapter-11"
grab luc-ch12-state-interest-areas           "https://pitkincounty.com/DocumentCenter/View/36085/chapter-12"
grab luc-ord-019-2026-amended-sections       "https://pitkincounty.com/DocumentCenter/View/36084/amended_sections--ord-019-2026"
echo DONE
