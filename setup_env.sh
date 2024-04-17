#!/bin/sh

# Create and activate virtual environment
if [ ! -d ".venv" ]; then
    python -m venv .venv/
fi
. .venv/bin/activate

# Install packages
pip install keyring
pip install requests_oauthlib
pip install pypubsub