#!/bin/bash
# Полный прогон для профиля. Использование: ./run.sh krakow-rent
PROFILE=${1:-warsaw-buy}
set -e

echo "=== Профиль: $PROFILE ==="
python3 scraper.py  --profile=$PROFILE --pages=1
python3 enrich.py   --profile=$PROFILE
python3 score.py    --profile=$PROFILE
