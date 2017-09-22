#!/usr/bin/env bash
set -e

### Prepare Python environment
python3 -m venv .venv --copies  # create a virtual environment
source .venv/bin/activate  # activate the environment
pip install -r requirements.txt  # install all dependencies