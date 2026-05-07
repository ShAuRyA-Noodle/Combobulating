# Vendored frontend libraries

We bundle React + ReactDOM + htm here so the venue stage demo runs **without
internet**. The team should download the three files once, commit them, and
never touch them again.

```bash
# Run once on a machine with internet (your laptop in the dorm).
cd aura/web/web/vendor
curl -L -o react.production.min.js \
  https://unpkg.com/react@18.3.1/umd/react.production.min.js
curl -L -o react-dom.production.min.js \
  https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js
curl -L -o htm.umd.js \
  https://unpkg.com/htm@3.1.1/dist/htm.umd.js
```

Verify all three are non-empty:

```bash
ls -lah aura/web/web/vendor/*.js
```

If any file is missing on stage, `app.js` will throw a clear error in the
console — the team should still keep a CDN-online fallback by editing
`index.html` to point the `<script>` tags at the unpkg URLs above.

## Why not a build step?

Stage demos must boot in <30 s on a machine the team has never touched. No
node, no npm, no Vite — just `bash run_local.sh`.
