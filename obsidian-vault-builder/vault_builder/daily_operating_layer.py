from __future__ import annotations

from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-daily-operating:start -->"
MANAGED_MARKER_END = "<!-- founderos-daily-operating:end -->"


def write_daily_operating_layer(config: BuilderConfig) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in daily_notes().items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def daily_notes() -> dict[str, str]:
    return {
        "Home.md": HOME_BLOCK,
        "01 Daily Notes/Today.md": TODAY,
        "01 Daily Notes/Founder Daily Dashboard.md": DAILY_DASHBOARD,
        "01 Daily Notes/Weekly Operating Review.md": WEEKLY_OPERATING_REVIEW,
        "00 Inbox/Source Intake Queue.md": SOURCE_INTAKE_QUEUE,
        "_Templates/Daily Operating Note Template.md": DAILY_OPERATING_TEMPLATE,
        "_Templates/Source Approval Plan Template.md": SOURCE_APPROVAL_TEMPLATE,
        "_Context Packs/daily-operating-context.md": DAILY_OPERATING_CONTEXT,
        "80 Databases/Operating.base": OPERATING_BASE,
    }


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"


HOME_BLOCK = """## Daily Operating Entry

- [[Today]]
- [[Founder Daily Dashboard]]
- [[Weekly Operating Review]]
- [[Source Intake Queue]]
- [[daily-operating-context]]

Use this entry when opening the vault. It keeps the working loop separate from source imports and preserves the rule that private/local data needs a separate source approval plan.
"""


TODAY = """## Start Here

### Current Operating Links

- [[Founder Daily Dashboard]]
- [[DocMind GTM Dashboard]]
- [[DocMind Publish Queue]]
- [[Source Index]]
- [[COMPLETION_AUDIT]]

### Today's Commitments

- [ ] One project output:
- [ ] One content/source output:
- [ ] One customer/discovery output:
- [ ] One system hygiene task:

### Capture

- 

### Decisions

- 

### Evidence To Link

- 

### End-of-Day Review

- What actually shipped?
- Which assumption became clearer?
- Which source or note should be linked?
- What should move to tomorrow?
"""


DAILY_DASHBOARD = """## Purpose

Operate FounderOS as a daily command surface: pick one high-leverage output, use source-grounded context, and avoid turning the vault into passive storage.

## Operating Stack

| Layer | Link | Use |
| --- | --- | --- |
| Today | [[Today]] | Capture and daily commitments |
| DocMind | [[DocMind GTM Dashboard]] | Current GTM and product wedge |
| Content | [[DocMind Publish Queue]] | Publish queue and source-grounded briefs |
| Research | [[Source Index]] | Public source notes and evidence |
| Context | [[daily-operating-context]] | Copy-ready AI context |
| Safety | [[GATE_STATUS]] | Import/network/privacy gate state |

## Daily Sequence

1. Open [[Today]].
2. Pick one output that can be finished today.
3. Check whether the task uses public notes only or needs a source approval plan.
4. Use [[Source Index]] before asking an AI tool to draft or decide.
5. End by linking the output back to a project, content note, decision, or review.

## Working Rules

- Keep private/local folders disabled unless an approved source plan exists.
- Do not paste private customer, email, chat, cookie, session, or credential data into AI tools.
- Mark unsupported claims as assumptions.
- Keep installs, trials, paid pilots, revenue, testimonials, and case studies at zero unless direct evidence exists.
"""


WEEKLY_OPERATING_REVIEW = """## Weekly Review

### Scoreboard

| Area | Target | Actual | Evidence |
| --- | ---: | ---: | --- |
| Project outputs shipped | 3 | 0 |  |
| Content drafts advanced | 2 | 0 |  |
| Customer/discovery actions | 5 | 0 |  |
| Source notes reviewed | 5 | 0 |  |
| Decisions updated | 1 | 0 |  |

### Review Questions

1. Which project moved forward in a visible way?
2. Which source cluster became useful?
3. Which content asset is closest to publishing?
4. Which customer pain or objection repeated?
5. Which assumption should be retired, strengthened, or tested?

### Next Week Focus

- Primary project:
- Primary output:
- Source cluster:
- Customer/discovery target:
- System hygiene:

### Safety Check

- Private/local sources enabled:
- Online AI/OCR/transcription/embedding:
- Manual review records:
- Any source approval plan needed:
"""


SOURCE_INTAKE_QUEUE = """## Purpose

Use this queue before enabling any new source. It is a planning surface, not an import area.

## Candidate Sources

| Source | Type | Risk | Why it matters | Status | Approval note |
| --- | --- | --- | --- | --- | --- |
| Browser bookmarks export | File export | Low | Public-ish saved URLs | Candidate | Needs exported HTML path |
| Readwise export | Folder export | Medium | Reading highlights | Candidate | Needs folder-specific plan |
| Notion export | Folder export | Medium | Project/source notes | Candidate | Needs export-only folder |
| Local project docs | Folder | Medium/high | Project context | Candidate | Must scope to README/docs only |

## Approval Checklist

- [ ] Exact read path:
- [ ] Exact write path:
- [ ] Whether file contents are read:
- [ ] Whether network is used:
- [ ] Whether anything is uploaded:
- [ ] Sensitive file patterns:
- [ ] Rollback path:
- [ ] Manual review criteria:
"""


DAILY_OPERATING_TEMPLATE = """---
type: daily_operating
date:
focus:
projects:
status:
tags:
  - daily-operating
---

# Daily Operating Note

## Commitments

- [ ] Project output:
- [ ] Content/source output:
- [ ] Customer/discovery output:
- [ ] System hygiene:

## Capture

## Decisions

## Source Links

## End-of-Day Review
"""


SOURCE_APPROVAL_TEMPLATE = """---
type: source_approval_plan
source_name:
source_type:
risk_level:
status: draft
tags:
  - source-approval
---

# Source Approval Plan

## Purpose

## Read Scope

- Path or URL:
- Include:
- Exclude:

## Write Scope

- Vault destination:
- Generated reports:
- Attachments copied:

## Network / Upload

- Network used:
- Uploads:
- Online AI/OCR/transcription/embedding:

## Risks

- Sensitive data risk:
- Secret risk:
- Customer/private data risk:

## Dry-Run Command

```bash
python scripts/scan_sources.py --config config/sources.yaml --dry-run
```

## Rollback

```bash
python scripts/rollback_import.py --last
```

## Approval

- Approved by:
- Approved at:
- Conditions:
"""


DAILY_OPERATING_CONTEXT = """## Copy-Ready Daily Operating Context

Use this with Codex, ChatGPT, Claude, or Claude Code when you want help planning or executing a day from the vault.

FounderOS is a privacy-first Obsidian vault. Current active source scope is public URL notes only. Private/local folders are disabled. Online AI, OCR, transcription, and embeddings are disabled in the builder config.

Daily operating pages:
- [[Today]]
- [[Founder Daily Dashboard]]
- [[Weekly Operating Review]]
- [[DocMind GTM Dashboard]]
- [[DocMind Publish Queue]]
- [[Source Intake Queue]]

Operating rules:
- Start from linked source notes and project pages.
- Mark unsupported claims as assumptions.
- Do not imply access to private customer, order, email, chat, cookie, session, credential, or local folder data.
- If a new source is needed, draft [[Source Approval Plan Template]] before scanning.
- Prefer one finished output over broad reorganization.

Useful prompts:

1. Review [[Today]] and propose one project output, one content output, and one customer/discovery output.
2. Turn [[DocMind Publish Queue]] into today's writing task without inventing proof.
3. Summarize [[Weekly Operating Review]] into next week's priorities.
4. Draft a source approval plan for a narrow exported source.
"""


OPERATING_BASE = """filters:
  and:
    - file.ext == "md"
    - or:
    - 'type == "daily_operating"'
    - 'type == "source_approval_plan"'
    - 'file.inFolder("01 Daily Notes")'
    - 'file.inFolder("00 Inbox")'
properties:
  file.name:
    displayName: File.Name
  type:
    displayName: Type
  date:
    displayName: Date
  focus:
    displayName: Focus
  status:
    displayName: Status
  risk_level:
    displayName: Risk Level
views:
  - type: table
    name: Operating
    order:
    - file.name
    - type
    - date
    - focus
    - status
    - risk_level
"""
