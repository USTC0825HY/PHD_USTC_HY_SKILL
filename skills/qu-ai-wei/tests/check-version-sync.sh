#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
exec "${QU_AI_WEI_PYTHON:-python}" "$DIR/tests/check_structure.py" version
