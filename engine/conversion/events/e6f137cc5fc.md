Google released **Chrome 151** to the stable channel on Wednesday, addressing **370 security vulnerabilities** — the largest single Chrome update of the year.

**Critical-severity bugs (7):**

- Four **use-after-free** flaws in Compositing, Views, Skia, and Ozone

- Two **insufficient validation of untrusted input** flaws in Dawn and ANGLE

- A **critical race condition** in Updater

**By severity:**

- 71 high-severity defects (use-after-free in Navigation, V8, Loader, Views, Autofill, Input, DataTransfer, DOM, ANGLE, Audio, Updater, Media; plus inappropriate implementation, type confusion, integer overflow, OOB read/write, policy bypass, race conditions, crypto flaws)

- 170 medium-severity weaknesses

- 122 low-severity defects

**Notable:** **30 vulnerabilities** impacted ANGLE (Almost Native Graphics Layer Engine) — Chrome's open-source WebGL backend for all graphics rendering. Google credited itself for finding **349 of 370 flaws** and paid external researchers **$58,500** in bug bounties.

Year-to-date, Google has resolved **over 1,800 vulnerabilities** in Chrome. Chrome 151 is now rolling out as v151.0.7922.71/.72 (Windows/macOS) and v151.0.7922.71 (Linux).

**Action:** Update browsers immediately — the volume of critical and high-severity flaws is exceptional even by Chrome standards. With 370 patches in one release, this is a strong signal about the complexity of modern browser attack surfaces.
