#!/bin/bash
# Push Slow Shakespeare to your Tidbyt
#
# First set your credentials:
#   export TIDBYT_DEVICE_ID="your-device-id"
#   export TIDBYT_API_TOKEN="your-api-token"

set -e
cd "$(dirname "$0")"

# Load credentials
source ~/.tidbyt_credentials

if [ -z "$TIDBYT_DEVICE_ID" ] || [ -z "$TIDBYT_API_TOKEN" ]; then
    echo "Missing credentials. Set them first:"
    echo ""
    echo "  export TIDBYT_DEVICE_ID=\"your-device-id\""
    echo "  export TIDBYT_API_TOKEN=\"your-api-token\""
    echo ""
    echo "Get these from the Tidbyt app: Settings > General > Get API Key"
    exit 1
fi

pixlet render slow_shakespeare.star
pixlet push "$TIDBYT_DEVICE_ID" slow_shakespeare.webp \
    --api-token "$TIDBYT_API_TOKEN" \
    --installation-id slowshakespeare

echo "✓ Pushed to Tidbyt"
