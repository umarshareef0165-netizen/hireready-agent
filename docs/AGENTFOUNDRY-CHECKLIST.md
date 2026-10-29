# AgentFoundry checklist — Code for a Billion (NOT DONE, NOT CLAIMED)

**Status on 2026-10-29: AgentFoundry usage has NOT been done and is NOT
claimed anywhere in this repo.** Nothing below may be written into the
submission as done until the step has actually been completed and its
evidence recorded in Section 6.

Sources used for this checklist (nothing else invented):
- Welcome email from Code for India (2026-10-28): "AgentFoundry.me is
  the official IDE of the hackathon. Install it, create a project,
  invite your teammates, and claim your 1 million free smart-code
  tokens to build your app or agent — then deploy on any cloud."
- Official page https://codeforindia.org/hackathon (re-checked
  2026-10-29): "Sign up on AgentFoundry.me, create a project in the
  IDE, invite collaborators, and get 1M smart-code tokens free";
  "How to participate: 1. Build in AgentFoundry, 2. Publish your repo,
  3. Record a demo, 4. Submit on GitHub"; "Projects must be deployed
  on any cloud and open-sourced"; submissions close 15 Nov 2026,
  winners 5 Dec 2026; sponsor award "Best Use of AgentFoundry Agents"
  is a separate recognition, not a guaranteed prize.

## 1. Sign up (browser step — not done by the preparer)
- [ ] Open https://agentfoundry.me (link from the welcome email).
- [ ] Sign up with umarshareef0165@gmail.com (the hackathon account).
      Do NOT create a second account under another email.
- [ ] Record: account created? (yes/no, date/time) — do not record any
      password anywhere. If signup asks for a card or payment at any
      point, STOP, enter nothing, report the exact prompt.

## 2. Create the project (browser step — not done)
- [ ] In the AgentFoundry IDE, create ONE project named
      "HireReady Agent" (suggested name; use the IDE's exact project
      field, do not invent a project ID).
- [ ] Impact area (must match the registration): Tech Employment
      for Youth. Problem statement: the one in
      `docs/SUBMISSION-DRAFT.md` (young people in Pakistan lacking
      practical, job-ready AI skills, mentorship, and a pathway to
      paid tech employment — no invented statistics).
- [ ] Teammates: NONE. Solo. Invite nobody without Umar Shareef's
      explicit approval for that person.

## 3. Claim the 1M free smart-code tokens (browser step — not done)
- [ ] Find and claim the 1 million free smart-code tokens in the IDE.
- [ ] Record the token balance shown AFTER claiming (screenshot or
      copied number, no secrets). If claiming asks for payment, a card,
      or a paid upgrade, STOP and report it — never buy tokens.
- [ ] Record how tokens are spent by the IDE (per build? per agent
      run?) only as the IDE itself displays it — do not guess a rate.

## 4. Get the existing code into AgentFoundry — OPEN QUESTION, verify live
The IDE's import path is NOT known from the welcome email or the
official page, so do not claim any of these until the IDE is open:
- [ ] Check, in this order, what the IDE actually offers:
      (a) import/link a GitHub repo
          (https://github.com/umarshareef0165-netizen/hireready-agent),
      (b) upload existing files, (c) paste/create files manually.
- [ ] Record the method actually used, and the AgentFoundry project
      URL if the IDE gives one. If NO import is offered, record that
      exactly and ask Umar Shareef before recreating the project
      by hand in the IDE — do not silently rebuild a second copy and
      then claim the two are "the same".
- [ ] Whichever method is used, the code that ships must be the
      tested code in this repo (`src/agent.py`, `src/server.py`,
      `public/index.html`, tests 9/9). Do not let the IDE silently
      rewrite the evidence rule (a skill is "evidenced" only with a
      real linked project/task).

## 5. Build / test inside AgentFoundry (browser step — not done)
- [ ] Inside the IDE, run the same end-to-end flow as
      `docs/DEPLOY-CARD-FREE.md` Section 4: gap → dated plan →
      portfolio → mock interview (visible rubric) → dashboard.
- [ ] Record: does the AgentFoundry copy produce the SAME gap result
      for the FitTrack test case as the local app? (yes/no, with the
      actual output pasted.) If it differs, the difference must be
      explained before submission — never submit two different apps
      as if they were one.
- [ ] Record whether any AgentFoundry "agent" feature (not just the
      IDE editor) was actually used. The sponsor award is called
      "Best Use of AgentFoundry Agents" — it may ONLY be mentioned in
      the submission if an AgentFoundry agent feature was genuinely
      used, with the feature named. Otherwise, do not mention it.

## 6. Evidence to record before ANY AgentFoundry claim is written
Create `docs/AGENTFOUNDRY-EVIDENCE.md` in this repo ONLY with facts
actually seen, in this shape (all fields blank until done):
- AgentFoundry account email: (blank)
- Project name / URL in the IDE: (blank)
- Token balance after claiming: (blank)
- Import method actually used: (blank)
- AgentFoundry copy test result (FitTrack case): (blank)
- AgentFoundry agent feature used, if any: (blank — "none" is a
  valid, honest answer)
Until that file is filled from live evidence, the submission must say
"AgentFoundry step pending" — never "built in AgentFoundry".

## 7. What AgentFoundry does NOT decide on its own
- Deployment: the official page says deploy "on any cloud" — the
  card-free deploy in `docs/DEPLOY-CARD-FREE.md` (PythonAnywhere
  primary) is the deployment, whether or not AgentFoundry is used.
  AgentFoundry alone, without a live deployed URL, does NOT satisfy
  "only deployed solutions count".
- Main prizes vs sponsor award: "Best Use of AgentFoundry Agents" is
  sponsor recognition on top of the four 25% judging criteria (size,
  severity, solution quality, proven impact). Using the IDE does not
  guarantee that award, and not using an agent feature does not by
  itself disqualify the main prizes — but that reading must be
  confirmed on the GitHub submission form at submit time, and the
  form's exact wording recorded, not assumed.
- NGO partner: the welcome email says "sign up with a local NGO or
  local partner of your choice". NO partner has been chosen by Umar
  Shareef and NONE is named in this checklist. Do not invent one.
  The partner question stays open until he names one (see Section 8).

## 8. Remaining chain after this checklist (none done)
1. Live deployment + end-to-end test (`docs/DEPLOY-CARD-FREE.md`).
2. AgentFoundry steps 1–6 above (browser, with his Gmail login).
3. Local NGO/partner OF HIS CHOICE — none named yet, none invented.
4. Small consented student pilot for honest dashboard counts —
   no pilot users exist yet, no stats invented; pilot only with
   consent, and only real in-app counts are reported.
5. Demo video: user records a real screen capture, 2–3 min, public,
   no credentials in any frame (script: `docs/DEMO-SCRIPT.md`).
6. Final GitHub-form submission — ONLY with Umar Shareef's approval,
   well before 15 Nov 2026, never in the final hour; after submission,
   do not change repo, video, or links.
