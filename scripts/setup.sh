#!/bin/bash
# Setup script for Gemini API skill

echo "Installing gemini-webapi..."

# Install base package
pip install gemini-webapi

# Install browser cookie support (optional but recommended)
pip install gemini-webapi[browser]

echo ""
echo "Setup complete! Now configure your cookies:"
echo ""
echo "1. Go to https://gemini.google.com and log in"
echo "2. Press F12 → Network tab → refresh"
echo "3. Copy the cookie values for __Secure-1PSID and __Secure-1PSIDTS"
echo ""
echo "Set environment variables:"
echo "  export GEMINI_1PSID='your_cookie_value'"
echo "  export GEMINI_1PSIDTS='your_cookie_value'"
echo ""
echo "Or add to your shell profile (~/.bashrc, ~/.zshrc):"
echo "  echo 'export GEMINI_1PSID=...' >> ~/.bashrc"