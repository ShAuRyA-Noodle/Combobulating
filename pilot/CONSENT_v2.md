# Aura Pilot — Participant Consent Form (v2, Wizard-of-Oz Lab Study)

Project: **Aura** (team Galaxy Brain, Thapar Institute of Engineering and Technology)
Study type: Unpaid academic research, not commercial
Pilot delivery: **Supervised in-person lab session on a team-owned iPhone** (no install on your phone)
Last updated: 2026-05-07
Replaces / amends: `pilot/consent_form.md` (v1, TestFlight). v1 remains in the repo for the audit trail; v2 is the form we actually sign at every session.

---

## 1. What changed from v1, in one paragraph

The v1 consent form assumed you would install Aura on your own phone via TestFlight for 7 days. We are not doing that any more. The team will not buy a paid Apple Developer account, so we cannot use TestFlight. Instead, you come to a quiet room for ~30 minutes (or ~90 minutes if you are one of the 8 longer-interview participants), and you use Aura on **our phone** while we sit with you. We record the screen and the audio so we can study it later. Your own phone stays in your pocket except during the first 8 minutes when we ask you to do five small tasks the way you usually would. **No app is installed on your phone.** **No data leaves our phone.** This is the safer of the two options and we should have started here.

---

## 2. What this is, in plain English

Hi. We are Shaurya and Shorya, two students at Thapar building an experimental phone assistant called Aura. Aura watches a few signals on a phone and tries to do small useful things — quiet a noisy WhatsApp group at the right moment, summarise the morning, flag a UPI debit that looks unusual, or suggest a breathing pause when the watch shows that heart-rate variability has dropped.

We are running a small in-person study to see if Aura actually helps. We need 30 people for short task-and-survey sessions, of whom 8 also stay for a longer interview. Everyone in the study is a friend or classmate — there is no payment, no Amazon voucher, no perk. You are helping us because you are kind and curious. That is the whole exchange.

This document tells you exactly what happens in the room, what we record, where the recording lives, and what your rights are. Read it slowly. If anything sounds off, tell us and we will fix it before you start.

---

## 3. What happens in the room

The session is **30 minutes** for the task-and-survey cohort, **90 minutes** for the qualitative-interview cohort.

| Step | Time | What happens |
|---|---|---|
| Welcome | 1 min | We say hi, offer water, clip a small mic to your shirt, and start the screen recording on a Mac that is mirroring our iPhone. |
| Consent | 3 min | We read the highlighted lines of this form aloud. You sign. We sign. Two copies. One stays with you. |
| Baseline tasks on your phone | 8 min | You do 5 small tasks (triage WhatsApp, check tomorrow's calendar, look at yesterday's spend, calm down after a short stress drill, pick which two notifications to reply to) on your own phone, the way you usually would. We may screen-record your phone too if you connect it to the Mac with a cable; if you would rather not, we just observe over your shoulder. |
| Aura tasks on our phone | 8 min | We hand you our iPhone (the demo device). You do the same five tasks using Aura. We are silent except for the start cue for each task. |
| Live diary | 3 min | You rate each task 1 to 5 for satisfaction. We write the numbers into a CSV. |
| Willingness-to-pay + open question | 5 min | We ask if you would pay ₹199/month for Aura, what your own price points are, and whether anything else is on your mind. |
| Wrap | 2 min | We stop the recording, save the file, offer to delete it on the spot if you want, thank you, and you go. |

For the 8 participants who agreed to the longer interview, after the wrap there is a 5-minute break and then a 60-minute conversation about what you noticed. Snacks on us.

---

## 4. What we record

Three things, and only these three:

1. **Screen video of our iPhone** for the 8 minutes you are using Aura, plus the room audio for the entire session. One MP4 file per participant. Stored on a team Mac SSD with a backup on an external SSD. Not on the cloud.
2. **Aura's own internal log** — the taps, timestamps, and reasoning traces Aura produced on our phone during your session. One JSON file per participant. Anonymised at export.
3. **Your survey answers** — the 1-to-5 ratings, the willingness-to-pay numbers, the open feedback. Captured on a Google Form on our laptop or on paper.

Optionally — only if you say yes — we also screen-record your **own phone** during the 8-minute baseline round, mirrored to our Mac via a USB cable that you plug into your phone. If you say no, we just observe your screen over your shoulder. That choice is on the checklist below.

We do **not** record:

- Anything before you arrive in the room or after you leave.
- Anything from your phone except the optional screen-share during the 8-minute baseline round.
- Any data from any account you do not authorise yourself in the moment.

---

## 5. What Aura sees on the demo device — and what it does not see

Aura on the demo phone has read access to:

| Source | Whose data | Why |
|---|---|---|
| **HealthKit on the demo phone** | Shaurya's own HealthKit record, not yours | We use Shaurya's HRV / sleep / steps as the demo input. You will see real numbers, but they are not your numbers. |
| **EventKit on the demo phone** | A test calendar with one seeded event for Task 2 | Task 2 demonstrates the morning brief on a fixture event we control. |
| **Gmail metadata** | A test Google account `aura.pilot.thapar@gmail.com` | Task 3 demonstrates receipt parsing on a fixture inbox. Not your Gmail. |
| **Notification panel on the demo phone** | Five seeded test notifications for Task 5 | Demonstrates the triage card on a fixture set. |

Aura on the demo phone does **not** see:

- Anything in your accounts.
- Anything on your phone.
- Your name, your number, your email — we never log them.

---

## 6. The data, after the session

- The MP4 video and the room audio are transcribed locally on our Mac using a free open-source tool called `whisper.cpp`. No cloud upload.
- The transcript is run through a redaction pass that masks phone numbers, email addresses, and your first name (taken from the consent form).
- The transcript and the redacted CSV are shared between Shaurya and Shorya for analysis. Nothing else leaves the team Mac.
- The raw audio is **deleted within 7 days** of the transcript being completed. The screen video is deleted at the end of the pilot, on **15 July 2026**, unless you ask us to delete it sooner.
- Anonymised aggregate numbers and de-identified short quotes may appear in the Phase 2 submission to Samsung EnnovateX 2026 and in a public GitHub repo. You see and approve any quote attributed to you before it is published.
- See `pilot/data_handling.md` for the full lifecycle.

---

## 7. Your rights, all of them

You can do any of the following at any time, without giving a reason:

- **Stop the session.** Say so. We stop. Your call about whether to keep or delete what we recorded so far.
- **Delete the recording on the spot.** At the wrap step we ask explicitly. If you want it gone, we delete it in front of you.
- **Withdraw later.** Email Shaurya at workwithshaurya10@gmail.com or message on WhatsApp. We delete every artefact within 7 days and confirm in writing. No questions.
- **See your own quote before it is used.** If we plan to use anything you said in the report or the deck, we send it to you for approval first.
- **Decline any single tick-box below.** Leaving a box unticked is a No. We respect that completely.

You do not need to finish the 30 minutes. Quitting partway is fine and does not affect the friendship.

---

## 8. Risks, honestly

- **Mild discomfort during Task 4.** Task 4 includes a short stressful drill (a timed quiz). It is mild and time-bounded. You can skip it; we log a `skipped` flag and move on. No pressure.
- **Embarrassment from being recorded.** Some people find the camera makes them self-conscious. The mic is small, the Mac screen faces away from you, and you can ask us to stop the recording at any point.
- **Time cost.** 30 minutes (or 90 minutes for the longer cohort). That is real time we are asking for. If today is bad, reschedule.
- **No physical risk.** No hardware on your body, no medical claim, no biometric measurement of you (the HRV demo uses Shaurya's data, not yours).

There is **no risk** of your own phone, your accounts, or your personal data being touched by Aura, because Aura is not running on your phone.

---

## 9. What we will do with the results

- Aggregate, anonymised numbers (means, percentages, charts) will appear in our Phase 2 submission to Samsung EnnovateX 2026.
- Anonymised raw CSVs (taps, times, success flags, satisfaction ratings) may be published in our public GitHub repo so judges can verify our claims. Your participant ID is `P001`–`P035`; no name, phone number, or email is in the CSV.
- Anonymised short quotes from your interview (qualitative cohort only) may appear in the report, with names changed and any identifying detail removed. You will see and approve any quote attributed to you before it is published.

---

## 10. Not commercial. Not paid.

This is academic coursework done as a hackathon entry. We are not a company. We are not paid for this. You are not paid for this. There is no incentive offered or implied. Aura may or may not become a real product later. If it does, your pilot data does not transfer to a future commercial entity without a separate, fresh consent.

---

## 11. Who to contact

- Shaurya Punj — workwithshaurya10@gmail.com — WhatsApp via Thapar contacts
- Shorya Gupta — Thapar contacts

If you would prefer to talk to a faculty member instead of us, email any Thapar ECE / CSE faculty and they can mediate.

---

## 12. Checkboxes — please tick what you agree to

Tick every box that applies. Leaving a box unticked is a No, and we respect that.

**Required to participate:**

- [ ] I have read this document. I understand what happens in the room, what is recorded, and where the recording lives.
- [ ] I consent to being **observed in person** by the researcher during the session.
- [ ] I consent to **screen recording of the demo iPhone** during the 8-minute Aura task round.
- [ ] I consent to **room audio recording** during the entire session, captured via the lavalier mic and the Mac.
- [ ] I consent to **local transcription** of the audio using `whisper.cpp` on the team Mac, and to **storage of the redacted transcript** on the team Mac and on a private GitHub repo branch shared between the two researchers.
- [ ] I understand this is **unpaid academic research** with no incentive.
- [ ] I understand I can **withdraw at any time** without giving a reason, and any artefacts I created will be deleted within 7 days.
- [ ] I understand my own phone is **not** touched by Aura, and **no app is installed** on my phone.

**Optional — tick if you are okay with each:**

- [ ] *(Optional)* I consent to **screen recording of my own phone** during the 8-minute baseline round (you connect your phone to the Mac with a USB cable). If unticked, the researcher will only observe over your shoulder.
- [ ] *(Qualitative cohort only)* I consent to a **60-minute audio-recorded interview** in the same session, after the 30-minute task block. The audio is transcribed locally and the raw audio is deleted within 7 days of transcription.
- [ ] *(Optional)* I consent to **anonymised short quotes** from my interview being included in the Phase 2 report and the public repo, after I have approved them.
- [ ] *(Optional)* I consent to my **first name** being listed in the public `THANKS.md` file in the repo.

**HRV pre/post sub-cohort (n=8) only:**

- [ ] *(Optional)* I will export my **own Apple Watch HealthKit data** (HRV, sleep, HR) for the 7 days surrounding this session and share the de-identified XML extract with the researchers. I understand the export contains only HR / HRV / sleep / step time-series, no identifying information, and I can review the file before sharing.

---

## 13. Signatures

| | Name (printed) | Signature | Date |
|---|---|---|---|
| Participant | ________________________ | ________________________ | __ / __ / 2026 |
| Researcher (Shaurya / Shorya) | ________________________ | ________________________ | __ / __ / 2026 |

Two copies. One stays with you. One stays in our locked folder on the team Mac, never on cloud.

---

End of consent form, version 2.
