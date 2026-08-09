from __future__ import annotations

from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-strategy-output:start -->"
MANAGED_MARKER_END = "<!-- founderos-strategy-output:end -->"


def write_strategy_outputs(config: BuilderConfig) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in strategy_notes().items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def strategy_notes() -> dict[str, str]:
    return {
        "10 Projects/DocMind/Decision - Support Automation Wedge.md": DOCMIND_DECISION,
        "10 Projects/221B/Decision - Evidence Ledger Wedge.md": B221_DECISION,
        "30 Content/SEO Briefs/Shopify Support Automation Brief.md": SHOPIFY_SUPPORT_BRIEF,
        "30 Content/SEO Briefs/Citation Verification Brief.md": CITATION_VERIFICATION_BRIEF,
        "50 AI Prompts & Workflows/Source-Grounded Research Workflow.md": SOURCE_GROUNDED_WORKFLOW,
    }


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"


DOCMIND_DECISION = """## Decision

Focus DocMind's first public product thesis on source-grounded support automation for Shopify merchants.

## Context

The current public source layer points toward Shopify customer accounts, order status surfaces, Flow automation, customer objects, and helpdesk/AI-agent workflows. This supports a wedge around improving support answers and workflows without replacing the merchant's whole helpdesk.

## Chosen Wedge

Start with source-grounded support automation: answer quality, policy/source citation, escalation, and repeated-question analysis.

## Why

- It is narrow enough to demo with public source notes.
- It aligns with Shopify merchant pain: order status, customer account questions, policy answers, and support follow-up.
- It avoids generic chatbot positioning.
- It creates a bridge into content, support QA, and help center improvement.

## Risks

- Existing helpdesks may already claim AI automation.
- Shopify support docs and customer data permissions need careful handling.
- The product needs trust signals before merchants let it answer customers.

## Next Actions

- Build a support workflow map for order status, returns, product questions, and account/profile support.
- Turn [[Shopify Support Automation Brief]] into a publishable SEO/content brief.
- Create a demo answer format with source citations and escalation rules.
"""


B221_DECISION = """## Decision

Explore 221B around an evidence ledger for AI research answers.

## Context

Public sources now include RAG, web search, citation attribution, RAGAS, attribution faithfulness, and AI agent workflow references. The strongest product direction is not generic search; it is auditability: what claim was made, which source supports it, and how reliable the support is.

## Chosen Wedge

Start with an evidence ledger: claims, sources, citation role, support level, contradictions, and open questions.

## Why

- It turns citation quality into a visible workflow.
- It can support research, SEO audits, and founder decisions.
- It pairs well with Codex/Claude workflows that can generate structured intermediate artifacts.

## Risks

- Citation verification can become too broad.
- The system needs clear definitions for source relevance versus claim support.
- Users may want polished answers before they value the ledger.

## Next Actions

- Build a reusable claim table template.
- Use the arXiv source notes as first evaluation examples.
- Turn [[Citation Verification Brief]] into a public article draft.
"""


SHOPIFY_SUPPORT_BRIEF = """## Content Brief

### Working Title

Shopify support automation: reduce repeated tickets without replacing your helpdesk

### Search Intent

The reader wants practical ways to automate repeated Shopify support questions, especially around order status, customer accounts, policies, and helpdesk workflows.

### Audience

Shopify founders, operators, and support leads at small ecommerce teams.

### Angle

Position DocMind as a source-grounded support layer: it uses merchant-approved sources, cites policies/docs, escalates uncertainty, and turns repeated questions into content and product improvements.

### Outline

1. Why repeated support questions drain founder/operator time.
2. Where Shopify support questions come from: customer accounts, order status, policy pages, and helpdesk conversations.
3. Why generic AI chat is risky for support.
4. A source-grounded workflow: source notes, answer rules, citations, escalation, analytics.
5. How to start with one workflow before automating everything.

### Source Notes

- [[Customer]]
- [[Sell on Shopify and support with Gorgias' helpdesk]]
- [[Gorgias- AI, Helpdesk & Chat - Instantly resolve support inquiries and grow your business. - Shopify App Store]]
- [[AI Agent explained Untitled]]

### CTA

Offer a lightweight support automation audit: repeated questions, missing source docs, risky answer areas, and first workflow candidate.
"""


CITATION_VERIFICATION_BRIEF = """## Content Brief

### Working Title

Citation is not verification: how to audit AI research answers

### Search Intent

The reader wants to know whether AI-generated citations actually support the claims in an answer.

### Audience

Founders, researchers, content strategists, and AI workflow builders.

### Angle

Use 221B as a practical evidence-ledger workflow: separate claims from sources, classify each citation's role, and mark unsupported claims before trusting the final narrative.

### Outline

1. Why AI answers can look sourced but still be unsupported.
2. The difference between source existence, relevance, and claim support.
3. Evidence ledger template: claim, source, citation role, support level, contradiction, confidence.
4. How this fits RAG and web search workflows.
5. How to use the workflow before publishing research or strategy.

### Source Notes

- [[Introduction to RAG - Developer Documentation]]
- [[Web search - OpenAI API]]
- [[.06635] Cited but Not Verified- Parsing and Evaluating Source Attribution in LLM Deep Research Agents contact arXiv subscribe to arXiv mailings]]
- [[.15217] Ragas- Automated Evaluation of Retrieval Augmented Generation open search open navigation menu contact arXiv subscribe to arXiv mailings]]
- [[2412.18004] Correctness is not Faithfulness in RAG Attributions contact arXiv subscribe to arXiv mailings]]

### CTA

Use an evidence ledger before turning AI research into product decisions or public content.
"""


SOURCE_GROUNDED_WORKFLOW = """## Workflow

### Goal

Turn public source notes into grounded project strategy, content briefs, and AI context packs.

### Inputs

- Source notes under [[Source Index]]
- Project pages: [[DocMind Home]], [[221B Home]]
- Context packs under `_Context Packs`

### Steps

1. Select a project and source cluster.
2. Extract claims, evidence, assumptions, and open questions.
3. Create or update a decision note.
4. Create a content brief if the source cluster maps to search intent.
5. Refresh the relevant context pack.
6. Run source index generation and final report.

### Verification

- Source notes exist.
- Claims are marked as evidence-backed or assumption.
- Private/local folders remain disabled unless explicitly approved.
- Generated notes use managed blocks so manual edits survive reruns.
"""
