#!/usr/bin/env bash
#
# resign_aura.sh
#
# Re-build and re-install the Aura iOS app on a connected iPhone using the
# free Apple ID Personal Team signing certificate. The Personal Team cert
# expires 7 days after issuance, so this script is run weekly during the
# pilot per ADR-0011 and aura/pilot/wizard_of_oz_protocol.md §5.
#
# Usage:
#   bash aura/scripts/resign_aura.sh
#
# Pre-requisites:
#   - macOS with Xcode 16 installed and command-line tools selected.
#   - The team Apple ID is already signed in to Xcode (Xcode > Settings > Accounts).
#   - The demo iPhone is connected via USB cable, unlocked, and "Trust this
#     computer" has been tapped at least once.
#   - The Aura Xcode project lives at apps/ios/Aura.xcodeproj relative to
#     the repository root.
#
# Exit codes:
#   0 — re-sign and install successful, log line appended
#   1 — pre-flight check failed (missing tool, no device, wrong directory)
#   2 — xcodebuild build failed
#   3 — xcodebuild exportArchive failed
#   4 — devicectl install failed
#   5 — log write failed
#
# This script is intentionally chatty. The pilot researcher reads the output
# and confirms each step before unplugging the iPhone.

set -euo pipefail

# ---------------------------------------------------------------------------
# CONFIG — edit these once per machine. Values below are the defaults for the
# team Mac. The Personal Team identifier is discoverable via:
#   security find-identity -v -p codesigning | grep "Apple Development"
# ---------------------------------------------------------------------------

# Personal Team identifier (10-character Apple Team ID associated with the
# Apple ID logged into Xcode > Settings > Accounts > Personal Team).
# Replace XXXXXXXXXX before first run.
PERSONAL_TEAM_ID="${AURA_PERSONAL_TEAM_ID:-XXXXXXXXXX}"

# Bundle identifier of the Aura app. Must match what is set in the Xcode
# target's General > Identity > Bundle Identifier.
BUNDLE_ID="${AURA_BUNDLE_ID:-com.galaxybrain.aura.dev}"

# Xcode scheme to build.
SCHEME="${AURA_SCHEME:-Aura}"

# Build configuration.
CONFIGURATION="${AURA_CONFIGURATION:-Release}"

# Path to the Aura Xcode project, relative to the repo root.
PROJECT_PATH="${AURA_PROJECT_PATH:-apps/ios/Aura.xcodeproj}"

# Working build directory for archives and exported .ipa files.
BUILD_DIR="${AURA_BUILD_DIR:-build/resign}"

# Re-sign log file (append-only).
RESIGN_LOG="${AURA_RESIGN_LOG:-aura/pilot/raw/_resign_log.txt}"

# Expected re-sign frequency (informational; printed at end).
RESIGN_FREQUENCY_DAYS=7

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log() {
    printf '[resign_aura] %s\n' "$*"
}

err() {
    printf '[resign_aura][ERROR] %s\n' "$*" >&2
}

# Repo root detection: walk up from the script's directory until we find a
# .git folder or the apps/ios directory. Works whether the script is invoked
# from the repo root or from inside aura/scripts/.
find_repo_root() {
    local dir
    dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/apps/ios" ] || [ -d "$dir/aura/apps/ios" ]; then
            printf '%s\n' "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    err "could not locate repo root from $(pwd)"
    return 1
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

preflight() {
    log "running pre-flight checks"

    if ! command -v xcodebuild >/dev/null 2>&1; then
        err "xcodebuild not found. Install Xcode 16 and run: sudo xcode-select --switch /Applications/Xcode.app"
        exit 1
    fi

    if ! command -v xcrun >/dev/null 2>&1; then
        err "xcrun not found. Xcode command-line tools are not selected."
        exit 1
    fi

    if [ "$PERSONAL_TEAM_ID" = "XXXXXXXXXX" ]; then
        err "PERSONAL_TEAM_ID is unset. Edit this script's CONFIG block or export AURA_PERSONAL_TEAM_ID."
        err "Discover your Personal Team ID with: security find-identity -v -p codesigning"
        exit 1
    fi

    REPO_ROOT="$(find_repo_root)"
    log "repo root: $REPO_ROOT"
    cd "$REPO_ROOT"

    # Resolve project path: either at <root>/<PROJECT_PATH> or <root>/aura/<PROJECT_PATH>
    if [ -d "$PROJECT_PATH" ]; then
        RESOLVED_PROJECT="$PROJECT_PATH"
    elif [ -d "aura/$PROJECT_PATH" ]; then
        RESOLVED_PROJECT="aura/$PROJECT_PATH"
    else
        err "Aura Xcode project not found at $PROJECT_PATH or aura/$PROJECT_PATH"
        exit 1
    fi
    log "Xcode project: $RESOLVED_PROJECT"

    # Detect connected iOS device. xcrun devicectl is available from Xcode 15+.
    log "detecting connected iOS device"
    if ! xcrun devicectl list devices 2>/dev/null | grep -E "iPhone|iPad" | grep -v "Simulator" >/dev/null; then
        err "no physical iOS device detected. Connect the demo iPhone via USB and unlock it."
        exit 1
    fi

    # Capture the first physical device's UDID for install step.
    DEVICE_UDID="$(xcrun devicectl list devices 2>/dev/null \
        | awk '/iPhone|iPad/ && !/Simulator/ {print $NF; exit}')"
    if [ -z "${DEVICE_UDID:-}" ]; then
        err "could not parse a device UDID from devicectl output"
        exit 1
    fi
    log "target device UDID: $DEVICE_UDID"

    mkdir -p "$BUILD_DIR"
    mkdir -p "$(dirname "$RESIGN_LOG")"

    log "pre-flight OK"
}

# ---------------------------------------------------------------------------
# Build (archive)
# ---------------------------------------------------------------------------

build_archive() {
    log "cleaning previous archive"
    rm -rf "$BUILD_DIR/Aura.xcarchive"

    log "running xcodebuild archive (this takes ~3 min on first run)"
    if ! xcodebuild \
        -project "$RESOLVED_PROJECT" \
        -scheme "$SCHEME" \
        -configuration "$CONFIGURATION" \
        -destination "generic/platform=iOS" \
        -archivePath "$BUILD_DIR/Aura.xcarchive" \
        DEVELOPMENT_TEAM="$PERSONAL_TEAM_ID" \
        CODE_SIGN_STYLE=Automatic \
        PRODUCT_BUNDLE_IDENTIFIER="$BUNDLE_ID" \
        archive; then
        err "xcodebuild archive failed"
        exit 2
    fi
    log "archive built at $BUILD_DIR/Aura.xcarchive"
}

# ---------------------------------------------------------------------------
# Export .ipa with Personal Team development signing
# ---------------------------------------------------------------------------

export_ipa() {
    log "writing exportOptions.plist"
    cat >"$BUILD_DIR/exportOptions.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>development</string>
    <key>teamID</key>
    <string>${PERSONAL_TEAM_ID}</string>
    <key>signingStyle</key>
    <string>automatic</string>
    <key>stripSwiftSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <false/>
</dict>
</plist>
PLIST

    log "exporting .ipa"
    rm -rf "$BUILD_DIR/export"
    if ! xcodebuild \
        -exportArchive \
        -archivePath "$BUILD_DIR/Aura.xcarchive" \
        -exportOptionsPlist "$BUILD_DIR/exportOptions.plist" \
        -exportPath "$BUILD_DIR/export"; then
        err "xcodebuild -exportArchive failed"
        err "common cause: Personal Team cert revoked or 3-app limit hit. Open Xcode > Settings > Accounts > Manage Certificates and revoke unused dev certs."
        exit 3
    fi

    IPA_PATH="$(find "$BUILD_DIR/export" -name "*.ipa" -type f | head -n 1)"
    if [ -z "${IPA_PATH:-}" ]; then
        err ".ipa not found under $BUILD_DIR/export"
        exit 3
    fi
    log "exported: $IPA_PATH"
}

# ---------------------------------------------------------------------------
# Install on device
# ---------------------------------------------------------------------------

install_on_device() {
    log "installing on device $DEVICE_UDID"
    if ! xcrun devicectl device install app \
        --device "$DEVICE_UDID" \
        "$IPA_PATH"; then
        err "devicectl install failed"
        err "if this is a fresh certificate, the user must manually trust it on the iPhone:"
        err "  Settings > General > VPN & Device Management > Apple Development > Trust"
        exit 4
    fi
    log "install complete"
}

# ---------------------------------------------------------------------------
# Append re-sign log entry
# ---------------------------------------------------------------------------

append_log() {
    local now next fingerprint
    now="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
    next="$(date -u -v+${RESIGN_FREQUENCY_DAYS}d +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null \
        || date -u -d "+${RESIGN_FREQUENCY_DAYS} days" +'%Y-%m-%dT%H:%M:%SZ')"

    fingerprint="$(security find-identity -v -p codesigning 2>/dev/null \
        | awk '/Apple Development/ {print $2; exit}')"
    fingerprint="${fingerprint:-unknown}"

    if ! printf '%s | team: %s | bundle: %s | cert: %s | next re-sign by: %s | device: %s\n' \
        "$now" "$PERSONAL_TEAM_ID" "$BUNDLE_ID" "$fingerprint" "$next" "$DEVICE_UDID" \
        >>"$RESIGN_LOG"; then
        err "could not append to $RESIGN_LOG"
        exit 5
    fi
    log "log entry appended to $RESIGN_LOG"
    log "next re-sign deadline: $next"
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

main() {
    log "starting Aura re-sign workflow"
    preflight
    build_archive
    export_ipa
    install_on_device
    append_log
    log "done. Open Aura on the demo iPhone, confirm HealthKit + EventKit permissions are still granted, run a smoke-test of one task, and you are good for the next ${RESIGN_FREQUENCY_DAYS} days."
}

main "$@"
