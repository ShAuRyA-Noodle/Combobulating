# Aura Architecture — Render Pipeline

Mermaid is the structural source of truth (`aura_architecture.mmd`). This
folder also holds the rendered SVG, the rendered PNG, and the JSON theme
config that locks the output to the deck's palette and font system. The
final styled artefact still lives in Figma — see
`aura_architecture_styling.md` for the re-style pass that ships into
slide 4 of the Phase 1 blueprint deck.

---

## Files

| File | Purpose |
|---|---|
| `aura_architecture.mmd` | Mermaid source. Edit this; everything else regenerates. |
| `aura_architecture_styling.md` | Figma re-style instructions. |
| `mermaid_config.json` | Light theme variables — locked palette, Inter Tight body. |
| `mermaid_config_dark.json` | Inverted variant for any dark surfaces. The deck is light, but a few internal review screens are dark. |
| `aura_architecture.svg` | Vector render, light theme, transparent background. Slide 4 import target. |
| `aura_architecture.png` | 1920 × 1080 raster fallback for Keynote / Slides where SVG import is flaky. |
| `aura_architecture_dark.svg` | Vector render, dark theme, transparent background. |

---

## One-time tool install

```
# Mermaid CLI (Node)
npm install -g @mermaid-js/mermaid-cli

# qrencode (used by /aura/design/qr/, not required for diagram render)
brew install qrencode
```

After install, verify:

```
mmdc --version    # → 11.x or newer
qrencode -V       # → 4.x
```

If `mmdc` is on your filesystem but not in PATH, the binary lives at
`$(npm prefix -g)/bin/mmdc`. Symlink into `/opt/homebrew/bin` if you
want it on your shell PATH:

```
ln -s "$(npm prefix -g)/bin/mmdc" /opt/homebrew/bin/mmdc
```

---

## Re-render after editing the .mmd source

Run from anywhere — the commands use absolute paths.

```
ARCH=/Users/shauryapunj/Desktop/Samsung\ Hack/aura/design/architecture

# 1. Vector SVG (light) — slide 4 import target
mmdc \
  -i "$ARCH/aura_architecture.mmd" \
  -o "$ARCH/aura_architecture.svg" \
  -c "$ARCH/mermaid_config.json" \
  -b transparent

# 2. Raster PNG fallback at 1920 x 1080
mmdc \
  -i "$ARCH/aura_architecture.mmd" \
  -o "$ARCH/aura_architecture.png" \
  -c "$ARCH/mermaid_config.json" \
  -b transparent \
  -w 1920 -H 1080
sips -z 1080 1920 "$ARCH/aura_architecture.png" \
  --out "$ARCH/aura_architecture.png"

# 3. Dark variant (rarely used)
mmdc \
  -i "$ARCH/aura_architecture.mmd" \
  -o "$ARCH/aura_architecture_dark.svg" \
  -c "$ARCH/mermaid_config_dark.json" \
  -b transparent
```

The `-b transparent` flag matters — slide 4 sits on the warm-paper
`#FAF8F5` background, and the diagram must layer cleanly without a
solid white block behind it.

The `sips -z H W` step normalises the PNG to exactly 1920 × 1080.
Mermaid's `-w/-H` flags set the SVG viewport but its puppeteer render
adds a 4–8 % padding margin, so the un-resampled PNG arrives at
~2013 × 1208. Resampling with `sips` is lossless from the perspective
of an SVG-rendered diagram (no anti-alias regressions visible at the
deck zoom levels).

---

## Verify the renders

```
xmllint --noout aura_architecture.svg          # silent → valid
xmllint --noout aura_architecture_dark.svg     # silent → valid
file aura_architecture.png                     # → "PNG image data, 1920 x 1080"
```

If `xmllint` is missing on a fresh Mac:

```
xcode-select --install
```

---

## Theme variables — what's locked

Both config files share the same locks. The only variable that flips
between light and dark is the colour pair `primaryColor` ↔ `lineColor`.

| Variable | Light value | Locked because |
|---|---|---|
| `background` | `transparent` | Slide composes the diagram over warm paper. |
| `primaryColor` | `#FAF8F5` | Node fill = warm paper. |
| `primaryTextColor` | `#0E0E0E` | Ink black for all labels. |
| `primaryBorderColor` | `#0E0E0E` | 1 px ink hairline strokes. |
| `lineColor` | `#0E0E0E` | Edge stroke colour. |
| `secondaryColor` | `#FF5B2E` | Sunset orange — only the orchestrator edge picks this up via the `classDef orange` directive in the .mmd. |
| `fontFamily` | `Inter Tight, Inter, system-ui, sans-serif` | Body sans per deck_spec.md §0. |

Mermaid's `theme: base` is the only theme that respects every variable
above without re-injecting its own greys.

---

## Troubleshooting font availability

Mermaid renders through headless Chromium (Puppeteer). The browser uses
whatever fonts are installed on the host machine, then falls back to
`system-ui` and finally generic `sans-serif` if Inter Tight is missing.

Symptoms and fixes:

| Symptom | Cause | Fix |
|---|---|---|
| Labels render in Helvetica or Arial-ish sans | Inter Tight not installed on the host | Install Inter Tight from Google Fonts (`brew install --cask font-inter-tight`) and re-run mmdc. |
| Letters render with wider glyphs than the Figma re-style | The host has Inter (the older Google sans) but not Inter Tight | Inter Tight is the locked face. Install it explicitly. The fallback Inter is acceptable for internal preview but not for deck export. |
| A label is cut off at the right edge | Long node label + Mermaid auto-sizing | Edit the .mmd to add a `<br/>` line break inside the node, then re-render. |
| The orchestrator edge is black, not orange | The `classDef orange` directive at the bottom of the .mmd was deleted | Restore the line `classDef orange stroke:#FF5B2E,stroke-width:3px;` and the `class ORCH orange` line beneath it. |
| `mmdc` fails with `Error: Failed to launch the browser process` | Puppeteer can't find Chromium | `npx puppeteer browsers install chrome` or set `PUPPETEER_EXECUTABLE_PATH` to a local Chrome / Chromium binary. |

The Figma re-style pass per `aura_architecture_styling.md` is the final
treatment — Mermaid's font choice and the auto-sized labels are only a
structural placeholder. If a label looks off in the raw render but the
.mmd reads correctly, do not edit the .mmd to fix the visual; fix it in
the Figma re-style.

---

## When to re-render

Re-render whenever any of the following changes in `aura_architecture.mmd`:

- A subgraph (`SENSE`, `INTELLIGENCE`, `EXPERIENCE`) gains or loses a node.
- An agent gains or loses a tool-call edge to the orchestrator.
- The orchestrator state list is revised.
- A surface (phone / watch / earbuds / tablet) is added or dropped.

Do **not** re-render to fix label spacing, arrow curvature, or colour —
those are downstream concerns owned by the Figma re-style pass.
