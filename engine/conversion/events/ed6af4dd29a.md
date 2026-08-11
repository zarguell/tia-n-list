*Underlying research broke Jul 29 (The Register, THN, Malwarebytes, CSO Online); it was missed by prior digests and only reached today's feed via a SOCFortress vendor summary. Surfaced now because the class remains unpatched and Microsoft-confirmed.*

Researcher **Håkon Måløy** (of the Morris II AI-worm lineage) demonstrated a **self-propagating prompt-injection worm in Microsoft Copilot for Word**, the third part of his "Context Collapse" series. The mechanism:

- Instructions hidden as **white-on-white text** (invisible to humans) are passed to the LLM **with formatting stripped**, so Copilot reads them as clear, authoritative commands — hijacking the user's original request (a **cross-domain prompt injection**, XPIA).

- **Stage 2 propagation:** the injected prompt commands Copilot to append the hidden payload to the documents it creates, framed as a "source-tracking/readability" requirement. The new file — authored by a trusted employee, clean of any malware signature — becomes a carrier that infects the next colleague's Copilot session via **Work IQ** scouting of OneDrive/SharePoint.

- **Demonstrated impact:** in a mock-company PoC, a hidden prompt silently **halved every numerical value in a financial report**, with the AI rewriting surrounding narrative so changes evaded attentive reviewers. No audit trail exists to show an external "scouted" document influenced the output.

**Status:** 144-day coordinated disclosure with Microsoft; Microsoft mitigated the *specific* PoC prompt, but **rewording the payload re-enabled propagation**, and the class survived model upgrades from GPT-4 through GPT-5.5/5.6. Microsoft confirmed the finding; no architectural fix exists because the model cannot structurally separate "data" from "instruction."

**Action:** Treat documents from outside the org — or from broad internal shares — as untrusted AI context; verify which files Copilot selects before generating; manually audit AI-produced financials against raw sources; push for provenance/metadata standards on AI-influenced documents.

---
