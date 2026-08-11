Arctic Wolf published a technical reverse-engineering analysis of the credential pipeline driving the FortiBleed campaign, revealing how the operator — tracked as an initial access broker on Russian-language forums — built a systematic credential factory using credential stuffing, password spraying, configuration harvesting, offline GPU cracking, and post-authentication traffic capture.

The campaign does not depend on a single malware payload but on an integrated pipeline: harvested configurations inform targeted password lists, 36-GPU rented clusters crack legacy salted SHA-256 hashes at 720 billion/second, and the FortigateSniffer tool (covered June 23) captures auth traffic from compromised devices. The data feeds ransomware affiliates through an IAB marketplace. The campaign has now been tracked for over a week, with CISA, Unit 42, Recorded Future, Hudson Rock, and now Arctic Wolf all publishing independent analyses — making this one of the most comprehensively documented credential-theft operations of 2026.

**Context:** *Previously tracked June 18–23 (initial disclosure, CISA warning, Unit 42 analysis, IAB attribution, GPU cluster mechanics, FortigateSniffer). New today: Arctic Wolf independent reverse-engineering of the full credential pipeline.*

---
