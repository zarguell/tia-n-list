Pillar Security demonstrated sandbox escapes in **Cursor, OpenAI Codex, Google Gemini CLI, and Antigravity** — without attacking the sandbox itself. The technique: the AI agent writes a file inside the workspace, then a trusted tool *outside* the sandbox (IDE extensions, Git hooks, VS Code task runner, language servers) reads and executes it. The agent follows every sandbox rule; the escape happens through the trust boundary between workspace files and host tools.

The research spans seven days of published write-ups. Key insight: sandboxing AI coding agents is insufficient when the agent's output files are implicitly trusted by the development toolchain. Organizations relying on AI coding agent sandboxes as a security boundary need to reassess.

Sources:
