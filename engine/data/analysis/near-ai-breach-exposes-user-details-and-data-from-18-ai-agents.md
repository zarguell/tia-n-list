NEAR AI disclosed a breach that exposed account information for about 100 users and data from 18 AI agents. The company said in a November 9 report that an attacker exploited a remote code execution vulnerability in SGLang, the open-source inference engine running on its servers.

The incident shows how AI infrastructure can become a breach path. SGLang is widely used to serve large language models, and a remote code execution flaw in that layer can expose both user data and the agents running on top of it.

NEAR AI has not published the full technical details in the available reports. Operators running SGLang should track the vendor advisory, review exposure of inference endpoints, and treat unauthenticated network access to model servers as a priority risk.