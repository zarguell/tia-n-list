# Claude Code Instructions

## Repository-Specific Guidance

### Pull Request Merging
When you need to merge pull requests (especially batch merging low-risk dependency updates), **ALWAYS** consult `MERGE_GUIDANCE.md` first. This file contains the fastest, most reliable approach for merging PRs using the GitHub CLI.

Key principles from MERGE_GUIDANCE.md:
- Use `gh` CLI directly, not GitHub MCP APIs
- Batch merge with one-liners using `xargs` or loops
- Handle conflicts by closing outdated PRs

**Do not skip this file** when working with PR merges. The documented approach has been tested and is significantly faster than trial-and-error with API calls.

## Repository Context

This is a Threat Intel Analyst news feed and blog powered by RSS and LLMs.

## Development Notes

- This repository uses automated dependency updates (Dependabot/Renovate)
- Dependency update PRs are generally low-risk and can be batch merged
- When in doubt about merging strategy, refer to MERGE_GUIDANCE.md
