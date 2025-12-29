#!/bin/bash

# Smoke test script for Flight Delay Prediction API
# Tests that the API is running and responding correctly

set -e

API_URL="http://localhost:8000"
ENDPOINT="${API_URL}/predict"

echo "Running smoke test against ${ENDPOINT}..."

# Test health endpoint first
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "${API_URL}/health" || echo "000")

if [ "$HEALTH_RESPONSE" != "200" ]; then
    echo "ERROR: Health check failed with status code: $HEALTH_RESPONSE"
    exit 1
fi

echo "Health check passed."

# Test predict endpoint
echo "Testing predict endpoint..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${ENDPOINT}" \
    -H "Content-Type: application/json" \
    -d '{"airport_code": "JFK"}' || echo -e "\n000")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" != "200" ]; then
    echo "ERROR: Predict endpoint failed with status code: $HTTP_CODE"
    echo "Response body: $BODY"
    exit 1
fi

echo "Predict endpoint test passed."
echo "Response: $BODY"

# Validate response contains expected fields
if echo "$BODY" | grep -q "airport_code" && \
   echo "$BODY" | grep -q "predicted_delay_minutes" && \
   echo "$BODY" | grep -q "delay_category"; then
    echo "Response structure validation passed."
else
    echo "ERROR: Response structure validation failed."
    exit 1
fi

echo "All smoke tests passed!"
exit 0

