#!/bin/bash
# Использование: ./run.sh [profile] [pages]
# Примеры:
#   ./run.sh krakow-rent 3
#   ./run.sh warsaw-buy
PROFILE=${1:-warsaw-buy}
PAGES=${2:-}
set -e

echo "=== Профиль: $PROFILE ==="
python3 scraper.py --profile=$PROFILE ${PAGES:+--pages=$PAGES}
python3 enrich.py  --profile=$PROFILE
python3 score.py   --profile=$PROFILE
