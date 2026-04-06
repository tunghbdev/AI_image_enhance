#!/usr/bin/env bash
set -e

mkdir -p weights

echo "[i] Downloading example weights (optional). Uncomment the lines once you have the URLs."
# Example (replace with your own mirrors):
# curl -L -o weights/dncnn_color.pth "https://your-host/dncnn_color.pth"
# curl -L -o weights/zerodce.pth "https://your-host/zerodce.pth"

echo "Done. Place weights under ./weights/ and restart the server."
