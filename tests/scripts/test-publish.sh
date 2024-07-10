#!/opt/homebrew/bin/bash

## Change the directory to root directory of the project
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(dirname "$(dirname "$SCRIPT_DIR")")
cd "${ROOT_DIR}" >/dev/null 2>&1 || { echo "[ERROR]: Failed to cd into root directory of the project" && exit 1; }

nvim pyproject.toml # Update the version
rm -rf dist/ # Delete previous builds
python3 -m build # Build
twine upload --repository testpypi dist/* # Upload to test.pypi
pip uninstall iitkgp_erp_login # Uninstall previous version
version=$(grep -i "version = " pyproject.toml | cut -d'"' -f2) # Get the latest version
pip install -i https://test.pypi.org/simple/ iitkgp-erp-login=="${version}" 2>/dev/null || echo "..." # Just ignore this
pip install -i https://test.pypi.org/simple/ iitkgp-erp-login=="${version}" # Get the latest version
