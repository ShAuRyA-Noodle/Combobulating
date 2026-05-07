#!/usr/bin/env bash
# Aura — single-command test orchestrator.
#
# Runs:
#   1. Lint           (black, ruff, mypy — best-effort)
#   2. Unit tests     (agents/, orchestrator/, memory/)
#   3. End-to-end     (e2e/)
#   4. Deck validate  (scripts/validate_deck.py)
#   5. iOS build      (xcodebuild — best-effort, skipped if Xcode missing)
#
# Each step prints its banner. Steps 1 and 5 are best-effort and never block;
# steps 2, 3, 4 are the hard gate — any failure exits non-zero.
#
# Usage:
#   bash scripts/run_all_tests.sh

set -u

# Resolve repo root from this script's location, regardless of cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON="${PYTHON:-python3}"
HARD_FAIL=0

banner() {
  printf '\n========== %s ==========\n' "$1"
}

# ---------------------------------------------------------------------------
# 1. Lint — best-effort
# ---------------------------------------------------------------------------

banner "1/5  LINT  (best-effort)"
LINT_DIRS="agents orchestrator memory e2e benchmarks scripts"

if command -v black >/dev/null 2>&1; then
  black --check ${LINT_DIRS} || echo "  [warn] black --check reported issues"
else
  echo "  [skip] black not installed"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff check ${LINT_DIRS} || echo "  [warn] ruff check reported issues"
else
  echo "  [skip] ruff not installed"
fi

if command -v mypy >/dev/null 2>&1; then
  mypy --ignore-missing-imports agents orchestrator memory \
    || echo "  [warn] mypy reported issues"
else
  echo "  [skip] mypy not installed"
fi

# ---------------------------------------------------------------------------
# 2. Unit tests — hard gate
# ---------------------------------------------------------------------------

banner "2/5  UNIT TESTS  (hard gate)"
if "${PYTHON}" -m pytest agents/ orchestrator/ memory/ -q; then
  echo "  [pass] unit tests green"
else
  echo "  [fail] unit tests red"
  HARD_FAIL=1
fi

# ---------------------------------------------------------------------------
# 3. End-to-end — hard gate
# ---------------------------------------------------------------------------

banner "3/5  END-TO-END  (hard gate)"
if "${PYTHON}" -m pytest e2e/ -q; then
  echo "  [pass] e2e green"
else
  echo "  [fail] e2e red"
  HARD_FAIL=1
fi

# ---------------------------------------------------------------------------
# 4. Deck validation — hard gate
# ---------------------------------------------------------------------------

banner "4/5  DECK VALIDATION  (hard gate)"
if "${PYTHON}" scripts/validate_deck.py; then
  echo "  [pass] deck checks clean"
else
  echo "  [fail] deck checks failed"
  HARD_FAIL=1
fi

# ---------------------------------------------------------------------------
# 5. iOS xcodebuild — best-effort
# ---------------------------------------------------------------------------

banner "5/5  iOS xcodebuild  (best-effort)"
if command -v xcodebuild >/dev/null 2>&1; then
  IOS_PROJ="$(find apps/ios -name '*.xcodeproj' -maxdepth 3 -print -quit 2>/dev/null || true)"
  if [ -n "${IOS_PROJ}" ]; then
    echo "  [info] building ${IOS_PROJ}"
    xcodebuild \
      -project "${IOS_PROJ}" \
      -scheme Aura \
      -sdk iphonesimulator \
      -configuration Debug \
      build 2>&1 | tail -20 \
      || echo "  [warn] xcodebuild reported issues (best-effort)"
  else
    echo "  [skip] no .xcodeproj found under apps/ios/"
  fi
else
  echo "  [skip] xcodebuild not installed (CI is Linux or Xcode missing)"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

banner "SUMMARY"
if [ "${HARD_FAIL}" -eq 0 ]; then
  echo "  ALL HARD-GATE STEPS GREEN."
  exit 0
else
  echo "  ONE OR MORE HARD-GATE STEPS FAILED."
  exit 1
fi
