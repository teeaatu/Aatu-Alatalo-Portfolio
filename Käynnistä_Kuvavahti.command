#!/bin/bash
cd "$(dirname "$0")" || exit 1
python3 "scripts/auto_upload_watch.py"
