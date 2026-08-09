# AI Workflow Library

## Prompt Library


## Agent Patterns


## Codex Workflows


## Claude Code Workflows


## ChatGPT Workflows


## Skill Specs


## Automation Ideas


## Failure Cases


## AI Prompts

<!-- founderos-public-workbench:start -->
## Public Workbench Snapshot

### Codex implementation loop

1. Define the goal and safety boundary.
2. Inspect existing files before changing behavior.
3. Write or update tests for the intended behavior.
4. Implement narrowly.
5. Run verification commands.
6. Update report/context pack with what changed.

### Research To Source Note

1. Add public URL to `data/urls.txt`.
2. Run dry-run scanner with network metadata only.
3. Review manual queue.
4. Import metadata source notes.
5. Link source notes to project and content pages.

### Context Pack Refresh

1. Read project home, decision notes, source index, and current public briefs.
2. Extract stable facts, assumptions, open questions, and active asks.
3. Keep private data out unless explicitly approved.
4. Produce a copy-ready context block.

### Failure Cases

- Importing duplicates because URL state is not idempotent.
- Treating a citation as evidence without checking claim support.
- Letting context packs become generic summaries instead of operational prompts.
- Scanning broad private folders before a source-specific plan.
<!-- founderos-public-workbench:end -->
