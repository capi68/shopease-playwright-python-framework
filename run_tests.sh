#!/bin/bash

# ShopEase — Test Runner
echo "ShopEase UI Test Runner"
echo "=========================="

APP_URL="http://localhost:5174"
MAX_RETRIES=30
RETRY_COUNT=0

echo "Checking if ShopEase is available..."
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -s "$APP_URL" > /dev/null 2>&1; then
    echo "ShopEase is running at $APP_URL"
    break
  fi
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "ShopEase is not responding at $APP_URL"
    echo "   Start it with: docker compose up --build -d"
    exit 1
  fi
  sleep 2
done

echo ""
echo "Running tests..."
echo ""

pytest tests/ \
  --alluredir=tests/allure-results \
  --clean-alluredir \
  -v \
  "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed!"
else
  echo "Some tests failed (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE
