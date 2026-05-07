# Aura — Sideload Guide (Secondary Path, Not Required)

A documented secondary path for participants who, after a lab session, want to keep Aura on their **own** iPhone past the 7-day Personal Team certificate window. This is **optional** and is **not part of the pilot data set**. The primary pilot delivery mechanism is the Wizard-of-Oz lab study on the team-owned demo iPhone (`wizard_of_oz_protocol.md`).

Reference: ADR-0011 §Alternatives (c).
Last updated: 2026-05-07
Owner: Shaurya Punj

---

## 1. Who this is for

You are reading this because:

- You completed an Aura lab session.
- You asked us at the wrap step whether you can keep Aura on your own iPhone.
- We said: yes, here is a free way to do it, but understand the caveats.

If you do not want to install anything on your own phone, ignore this guide. Nothing in your pilot participation requires it.

---

## 2. The two free routes

There are two free routes. Both use your own Apple ID Personal Team certificate, which expires every 7 days, so both require weekly re-signing.

### Route A — direct from Xcode (you have a Mac)

Best for: anyone who has access to a Mac with Xcode 16 installed (a friend's Mac is fine). Cleanest, fewest steps.

**You will need:**

- A Mac running macOS 14+ with Xcode 16 installed (free from the App Store, ~10 GB).
- Your own Apple ID (free) signed in to Xcode at Xcode → Settings → Accounts.
- A Lightning-to-USB or USB-C cable.

**Steps:**

1. Clone the Aura repo: `git clone https://github.com/galaxy-brain/aura.git`
2. Open `aura/apps/ios/Aura.xcodeproj` in Xcode 16.
3. In the project navigator, click the Aura target → Signing & Capabilities tab.
4. Set **Team** to your own "Personal Team — your name (Personal Team)".
5. Change **Bundle Identifier** to something globally unique using your own initials, e.g. `com.<your-initials>.aura.dev`. The free Personal Team allows up to 3 unique bundle IDs per Apple ID, so do not pick one you might want to reuse for another sideloaded app.
6. Connect your iPhone with the cable. Trust the Mac when prompted on the iPhone.
7. In Xcode, select your iPhone in the device dropdown at the top of the window.
8. Press the Play button (Run). First build takes ~3 minutes.
9. The first time the app installs on your iPhone, iOS will block it. Open Settings → General → VPN & Device Management → tap your Apple ID under Developer App → Trust.
10. Open Aura, grant HealthKit / EventKit / Notifications permissions when asked. Sign in with your own Google account if you want CommsAgent to read your real Gmail metadata.

**Re-signing every 7 days:** repeat steps 6–8 once a week. Aura will silently refuse to launch the day the certificate expires. There is no over-the-air update.

### Route B — AltStore + AltServer (you do not have a Mac)

Best for: you do not have access to a Mac, but you do have a Windows or Linux laptop on the same Wi-Fi as your iPhone.

**You will need:**

- A Windows 10/11 or macOS / Linux laptop on the same Wi-Fi network as your iPhone, with **iTunes** (Windows) or the system tools (macOS) installed.
- Your own Apple ID (free).
- An `Aura.ipa` file built and provided by us. We can build a generic `.ipa` for you using your Apple ID and email it (the build is signed with your Personal Team cert, not ours, so we need your Apple ID password — which we strongly prefer not to handle. **The recommended path is Route A**; Route B exists for completeness only.)

**Steps (high level):**

1. Install AltServer from `https://altstore.io/` on your laptop. Free, open source.
2. Connect your iPhone to your laptop via cable. Run AltServer.
3. AltServer installs AltStore on your iPhone.
4. Inside AltStore on your iPhone, sign in with your own Apple ID.
5. Use AltStore → My Apps → "+" → select the Aura `.ipa` we provided.
6. AltStore signs the `.ipa` with your Personal Team cert and pushes it to your iPhone.
7. Trust the developer profile on the iPhone (Settings → General → VPN & Device Management → Trust).
8. Open Aura.

**Re-signing every 7 days:** AltServer must be running on your laptop, on the same Wi-Fi as your iPhone, **at least once every 7 days** to refresh the cert via background AltStore activity. If you forget for too long, the app stops launching and you have to manually re-sign from AltStore.

---

## 3. What you should know before you sideload

Honest caveats. Read these.

- **The build expires every 7 days.** This is an Apple platform constraint on the free Personal Team certificate. There is no workaround except buying the Apple Developer Program (USD 99/year), which the team has chosen not to do (`docs/decisions/ADR-0011-no-apple-developer-program.md`).
- **You are responsible for re-signing.** We are not.
- **Some entitlements are limited on the free tier.** Apple disables certain capabilities for Personal Team apps — most notably background audio, push notifications via APNs, HealthKit background delivery beyond the foreground, and several iCloud entitlements. Aura's foreground features (Brief card, Reasoning Trace, manual triage) all work; some background loops may be quiet until the app is opened.
- **Your data goes nowhere we can see.** Aura on your phone is the same on-device-only build (`docs/decisions/ADR-0005-on-device-only.md`). We get no telemetry from a sideload. If you want to share your usage data with us for the pilot, you have to export it yourself and send it (we will not ask).
- **This is not a TestFlight build, not an App Store build, not a beta program you are enrolled in.** It is a developer build signed with *your* Personal Team certificate and run on *your* phone. You can delete it any time; the cert and any data go with it.
- **Sideloaded data is not part of the pilot data set.** Anything you do with Aura on your own phone after the lab session does not feed into the n=30 quant analysis or the n=8 qual analysis. We chose to keep the pilot data set clean — only the supervised lab sessions count.

---

## 4. Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| "Untrusted Developer" dialog when launching Aura | First-launch trust step skipped | Settings → General → VPN & Device Management → tap your Apple ID → Trust |
| Aura silently refuses to open after a few days | Personal Team cert expired (7-day window) | Re-run Route A steps 6–8 or Route B re-sign |
| Xcode says "Maximum App IDs limit reached" | Free Personal Team allows 3 app IDs per 7-day window | Wait 7 days, or revoke an unused dev cert at Xcode → Settings → Accounts → Manage Certificates |
| Build fails with "No profile for team … matching … found" | Bundle ID conflicts with another sideloaded app on the same Apple ID | Change Bundle Identifier to something globally unique with your initials |
| HealthKit data not appearing in Aura | Permission not granted on first launch | Settings → Privacy & Security → Health → Aura → enable all categories |
| AltStore says "AltServer not found" | Laptop and iPhone on different Wi-Fi networks, or AltServer not running | Confirm same Wi-Fi; restart AltServer; restart AltStore |

---

## 5. Removing Aura

To remove Aura from your iPhone completely:

1. Long-press the Aura icon → Remove App → Delete App. This wipes the on-device store immediately (ADR-0007 — the SQLCipher database is encrypted to the Secure Enclave key tied to the app's keychain, which iOS purges on uninstall).
2. Settings → General → VPN & Device Management → tap your Apple ID profile → Remove Profile. This revokes the Personal Team cert from your device.
3. (Optional, Route A) Remove the project from Xcode → Settings → Accounts if you want a clean Apple ID state.

Done. There is no residue. There is no cloud account to delete because Aura never had one.

---

## 6. We are happy to help — within limits

If you want to sideload Aura and you hit a snag, message Shaurya on WhatsApp and we will help with Route A on your friend's Mac in person if you bring it to a coffee at the campus cafe. We will not ask for your Apple ID password and we will not ask for your phone unlocked overnight. The sideload is yours to own.

If you would rather just see Aura again at a follow-up lab session, that is fine too — message us and we will book a slot.

---

End of sideload guide.
