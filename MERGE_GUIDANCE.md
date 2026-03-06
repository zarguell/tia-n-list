# Pull Request Merge Guidance

## Quick Batch Merge Strategy

When you need to merge multiple pull requests quickly (especially low-risk dependency updates like Dependabot/Renovate PRs), use this approach:

### Step 1: List All Open PRs
```bash
gh pr list --repo [owner]/[repo]
```

### Step 2: Merge All PRs in Batch
```bash
# Get all PR numbers and merge them using xargs
gh pr list --json number --jq '.[].number' --repo [owner]/[repo] | xargs -I {} gh pr merge {} --squash --repo [owner]/[repo]
```

### Alternative: For Loop
```bash
# If xargs has issues, use a for loop
gh pr list --json number --jq '.[].number' --repo [owner]/[repo] | while read pr; do
    gh pr merge "$pr" --squash --repo [owner]/[repo]
done
```

### Step 3: Update Stale PR Branches
If any PRs fail to merge due to "Base branch was modified" errors, update their branches first:
```bash
# Update all open PR branches to latest main
gh pr list --json number --jq '.[].number' --repo [owner]/[repo] | while read pr; do
  echo "Updating branch for PR #$pr..."
  gh pr update-branch "$pr" --repo [owner]/[repo] || echo "Failed to update PR #$pr"
done

# Retry merging the updated PRs
gh pr list --json number --jq '.[].number' --repo [owner]/[repo] | xargs -I {} gh pr merge {} --squash --repo [owner]/[repo]
```

### Step 4: Handle True Conflicts
If any PRs still fail after branch updates (actual merge conflicts, not just stale branches):
```bash
# List remaining open PRs
gh pr list --repo [owner]/[repo]

# Close outdated/conflicted PRs
gh pr close [pr-number] --repo [owner]/[repo] --comment "Superseded by newer merged PRs"
```

## Why This Approach?

- **Fast**: Uses `gh` CLI directly, no API overhead or complex parsing
- **Simple**: One-liner commands, minimal troubleshooting
- **Safe**: Squash merge keeps history clean
- **Transparent**: Shows exactly what's being merged

## What NOT to Do

- Don't use GitHub MCP APIs for batch operations (returns massive JSON, slow parsing)
- Don't manually merge each PR individually (slow)
- Don't use complex Python/jq parsing when `gh` has built-in JSON support

## Example for This Repository

```bash
# Attempt to merge all open PRs
gh pr list --json number --jq '.[].number' --repo zarguell/tia-n-list | xargs -I {} gh pr merge {} --squash --repo zarguell/tia-n-list

# If "Base branch was modified" errors occur, update PR branches and retry:
gh pr list --json number --jq '.[].number' --repo zarguell/tia-n-list | while read pr; do
  gh pr update-branch "$pr" --repo zarguell/tia-n-list
done
gh pr list --json number --jq '.[].number' --repo zarguell/tia-n-list | xargs -I {} gh pr merge {} --squash --repo zarguell/tia-n-list

# If true conflicts occur, close outdated PRs
gh pr close [pr-number] --repo zarguell/tia-n-list --comment "Superseded by newer merged PRs"
```
