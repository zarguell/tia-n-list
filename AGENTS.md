## Project Structure
- Specs: @docs/architecture.md, @docs/tasks.md
- Source: src/ (Python automation scripts)
- Config: config/ (YAML files for feeds and prompts)
- Site: hugo/ (Hugo static site content and templates)
- Tests: tests/

## Key Context
- Architecture: @docs/architecture.md
- Tasks: @docs/tasks.md
- Patterns & Conventions: @docs/.context.md
- History & Decisions: @docs/.memory.md

## Commands
- `pytest tests/`
- `mypy src/`
- `ruff check src/`
- `hugo -s hugo/`

## Workflow
1. Read @docs/architecture.md for project requirements.
2. Select a task from @docs/tasks.md.
3. Implement tests first in the `tests/` directory.
4. Write source code in `src/` to make tests pass.
5. Run validation commands and mark the task as complete.
6. Update any mistakes, lessons learned, decisions, in @docs/.memory.md.
7. Update any most important patterns and conventions in @docs/.context.md