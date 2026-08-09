from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-completion:start -->"
MANAGED_MARKER_END = "<!-- founderos-completion:end -->"


def write_completion_outputs(
    config: BuilderConfig,
    inventory_count: int,
    source_count: int,
    manual_review_count: int,
) -> list[Path]:
    bodies = completion_notes(inventory_count, source_count, manual_review_count)
    written: list[Path] = []
    for relative_path, body in bodies.items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def completion_notes(inventory_count: int, source_count: int, manual_review_count: int) -> dict[str, str]:
    generated = datetime.now().isoformat(timespec="seconds")
    return {
        "Home.md": home_dashboard(inventory_count, source_count, manual_review_count),
        "_Indexes/Master Index.md": master_index_dashboard(inventory_count, source_count, manual_review_count),
        "_System/OPERATING_MANUAL.md": operating_manual(),
        "_System/SETUP_COMPLETE.md": setup_complete(generated, inventory_count, source_count, manual_review_count),
        "_System/BLOCKED_SOURCES.md": blocked_sources(),
    }


def home_dashboard(inventory_count: int, source_count: int, manual_review_count: int) -> str:
    return f"""## FounderOS Operating Dashboard

### Setup State

- Public inventory records: {inventory_count}
- Imported source notes: {source_count}
- Active manual-review records: {manual_review_count}
- Private/local folders: disabled
- Online AI/OCR/transcription: disabled

### Start Here

- [[DocMind Home]]
- [[DocMind GTM Dashboard]]
- [[221B Home]]
- [[Source Index]]
- [[AI Workflow Library]]
- [[OPERATING_MANUAL]]
- [[SETUP_COMPLETE]]

### This Week's Operating Loop

1. Review [[Source Index]] and pick one source cluster.
2. Update a project decision or content brief.
3. Refresh the relevant context pack.
4. Keep private data out unless a separate source plan is approved.
"""


def master_index_dashboard(inventory_count: int, source_count: int, manual_review_count: int) -> str:
    return f"""## Generated Master Dashboard

### Counts

- Public inventory records: {inventory_count}
- Source notes: {source_count}
- Manual-review records: {manual_review_count}

### Core Maps

- [[Source Index]]
- [[DocMind Index]]
- [[221B Index]]
- [[AI Workflow Index]]
- [[Content Index]]
- [[Research Index]]

### Working Outputs

- [[DocMind GTM Dashboard]]
- [[DocMind Publish Queue]]
- [[DocMind Customer Interview Log]]
- [[DocMind Lead Follow-Up Tracker]]
- [[Decision - Support Automation Wedge]]
- [[Decision - Evidence Ledger Wedge]]
- [[Shopify Support Automation Brief]]
- [[Citation Verification Brief]]
- [[Source-Grounded Research Workflow]]
"""


def operating_manual() -> str:
    return """## Daily operating loop

1. Capture raw ideas in [[Inbox]] or daily notes.
2. Link project-relevant items to [[DocMind Home]] or [[221B Home]].
3. Use [[Source Index]] before asking an AI tool to draft strategy, content, or research.
4. Promote useful ideas into a decision note, source note, research note, or content brief.

## Weekly review loop

1. Review [[Master Index]], [[Source Index]], project homes, and decision notes.
2. Identify stale assumptions, unsupported claims, and next experiments.
3. Refresh context packs for the active project.
4. Choose one content brief or product experiment to advance.

## Public source update loop

1. Add public URLs to `obsidian-vault-builder/data/urls.txt`.
2. Run dry-run scan, privacy review, dedupe, import plan, and confirmed import.
3. Regenerate source indexes, strategy outputs, public workbench, completion outputs, and reports.
4. Keep blocked pages documented in [[BLOCKED_SOURCES]].

## Private source rule

Private/local folders remain disabled. Before any local/private source is used, create a folder-specific plan that states read paths, write paths, network/upload behavior, risks, and rollback.

## AI usage rule

Context packs are safe to copy into AI tools because they are built from public sources and manually written strategy notes. Do not paste private data unless a separate approval exists.
"""


def setup_complete(generated: str, inventory_count: int, source_count: int, manual_review_count: int) -> str:
    return f"""## Setup status: complete

Generated at: {generated}

## Evidence

- Vault scaffold exists.
- Templates exist.
- Obsidian Bases scaffold exists.
- Source notes imported from public URL list.
- Source-driven indexes exist.
- Public workbench pages exist.
- Strategy decisions and SEO briefs exist.
- DocMind GTM dashboard, publish queue, customer interview log, lead tracker, and templates exist.
- Context packs exist.
- Import system supports dry-run, audit, idempotent import, and rollback.

## Counts

- Public inventory records: {inventory_count}
- Imported source notes: {source_count}
- Active manual-review records: {manual_review_count}

## Safety boundary

- Private/local folders are disabled.
- Browser cookies, sessions, passwords, Keychain, email, and chats were not read.
- Online AI, OCR, transcription, and embeddings are disabled.
- Original files are not deleted, moved, renamed, or overwritten.

## Remaining gated work

Local/private sources are intentionally outside this completed setup state until a separate source plan is approved.
"""


def blocked_sources() -> str:
    return """## Superseded blocked public sources

The following public URLs were removed from active scanning because they returned 403 challenge pages during metadata-only fetches. They are retained here for auditability and replaced by accessible official/developer sources where possible.

### OpenAI

- Blocked: `https://openai.com/index/harness-engineering`
- Blocked: `https://openai.com/codex/`
- Replacement: `https://developers.openai.com/codex`
- Replacement: `https://developers.openai.com/codex/guides/agents-md`

### Shopify

- Blocked: `https://help.shopify.com/en/manual/customers/customer-service`
- Blocked: `https://help.shopify.com/en/manual/shopify-flow`
- Blocked: `https://help.shopify.com/en/manual/customers/customer-accounts/new-customer-accounts`
- Replacement: `https://shopify.dev/docs/apps/build/customer-accounts`
- Replacement: `https://shopify.dev/docs/apps/build/flow`
- Replacement: `https://shopify.dev/docs/apps/launch/distribution/support-your-customers`

## Policy

Do not attempt to bypass challenge pages, cookies, sessions, or login gates. Use public accessible alternatives or leave the source documented for manual review.
"""


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"
