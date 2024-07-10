#!/bin/bash

## Change the directory to root directory of the project
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(dirname "$(dirname "$SCRIPT_DIR")")
cd "${ROOT_DIR}" >/dev/null 2>&1 || { echo "[ERROR]: Failed to cd into root directory of the project" && exit 1; }

# cp -a ./src/iitkgp_erp_login/* ./venv/lib/python3.*/site-packages/iitkgp_erp_login/
cp -a ./src/iitkgp_erp_login/* /opt/homebrew/lib/python3.*/site-packages/iitkgp_erp_login/
