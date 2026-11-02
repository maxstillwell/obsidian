from __future__ import annotations

from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-public-workbench:start -->"
MANAGED_MARKER_END = "<!-- founderos-public-workbench:end -->"


def write_public_workbench(config: BuilderConfig) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in workbench_notes().items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        updated = _upsert_managed_block(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def _upsert_managed_block(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    if existing.strip():
        return f"{existing.rstrip()}\n\n{block}"
    title = _title_from_body_or_path(body)
    return f"# {title}\n\n{block}"


def _title_from_body_or_path(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "FounderOS Public Workbench"


def workbench_notes() -> dict[str, str]:
    return {
        "10 Projects/DocMind/DocMind Home.md": DOCMIND_HOME_BLOCK,
        "10 Projects/DocMind/Public Research Brief.md": DOCMIND_RESEARCH_BRIEF,
        "10 Projects/221B/221B Home.md": B221_HOME_BLOCK,
        "10 Projects/221B/Public Research Brief.md": B221_RESEARCH_BRIEF,
        "30 Content/Content Engine Home.md": CONTENT_ENGINE_BLOCK,
        "30 Content/Public Content Operating System.md": CONTENT_OPERATING_SYSTEM,
        "50 AI Prompts & Workflows/AI Workflow Library.md": AI_WORKFLOW_BLOCK,
        "50 AI Prompts & Workflows/Public AI Workflow Operating System.md": AI_WORKFLOW_OPERATING_SYSTEM,
        "20 Research/Research Map.md": RESEARCH_MAP_BLOCK,
        "20 Research/Public Source Map.md": PUBLIC_SOURCE_MAP,
        "_Context Packs/docmind-context.md": DOCMIND_CONTEXT_BLOCK,
        "_Context Packs/221b-context.md": B221_CONTEXT_BLOCK,
        "_Context Packs/content-strategy-context.md": CONTENT_CONTEXT_BLOCK,
        "_Context Packs/ai-workflow-context.md": AI_WORKFLOW_CONTEXT_BLOCK,
        "_Context Packs/current-projects-context.md": CURRENT_PROJECTS_CONTEXT_BLOCK,
        "_Context Packs/research-context.md": RESEARCH_CONTEXT_BLOCK,
    }


DOCMIND_HOME_BLOCK = """## Public Workbench Snapshot

### Product Thesis

DocMind should be treated as a Shopify support automation workspace: it helps merchants turn help docs, policies, product knowledge, and support patterns into fast, source-grounded answers and operational improvements.

### ICP

- Shopify founder/operators with recurring support tickets and limited support headcount.
- Small ecommerce teams that already use a helpdesk but still have inconsistent answers, stale docs, or weak visibility into repeated customer pain.
- Stores where support quality affects conversion, retention, refunds, and repeat purchase.

### Customer Pain Points

- Repetitive tickets consume founder or agent time.
- Answers vary by agent because policy and product knowledge are scattered.
- Help center content becomes stale and does not reflect real customer questions.
- Support data rarely turns into SEO briefs, product fixes, or onboarding improvements.
- AI support tools create trust concerns unless answers cite the source and escalate gracefully.

### SEO Strategy

- Cluster 1: Shopify customer support automation.
- Cluster 2: AI helpdesk and AI support workflows for ecommerce.
- Cluster 3: Order status, returns, exchanges, shipping, and policy automation.
- Cluster 4: Support analytics turned into content and product decisions.
- Cluster 5: Comparisons against helpdesk incumbents without positioning as a generic ticketing system.

### Growth Experiments

- Publish one pain-led SEO brief per repeated support workflow.
- Offer a lightweight support audit for Shopify stores: top repeated tickets, missing docs, and automation opportunities.
- Build source-grounded demo flows around shipping, returns, product questions, and order-status support.
- Create comparison pages around "AI layer on top of existing helpdesk" rather than "replace your helpdesk."

### Sales Objections

- "We already use Gorgias/Zendesk/Intercom."
- "AI will hallucinate support answers."
- "Setup will take too long."
- "Our policies and catalog change often."
- "We cannot risk customer data leakage."

### Roadmap

- Now: public research, ICP notes, support workflow taxonomy, source-grounded answer demo.
- Next: Shopify/helpdesk connector plan, citation-first answer QA, escalation workflow, content cluster.
- Later: support analytics, recommendation loops, experiment reporting, team workflow controls.

### AI Prompts

- Turn these customer pain points into five SEO briefs for Shopify merchants.
- Create a demo support workflow that cites source policy notes before answering.
- Compare DocMind against a generic AI chatbot and identify positioning gaps.
- Extract the riskiest assumptions in this product thesis.
"""


DOCMIND_RESEARCH_BRIEF = """# DocMind Public Research Brief

## Working Question

What public evidence supports a focused product around Shopify support automation, source-grounded answers, and support-to-growth workflows?

## Research Buckets

- Shopify operations: support, order management, returns, shipping, product discovery, customer service.
- Helpdesk incumbents: positioning, app store language, integrations, automation claims.
- AI support risk: hallucination, escalation, privacy, source citation, QA.
- SEO demand: pain-led queries from merchants and support teams.

## Evidence To Add

- Public docs and app listing notes under [[Source Index]].
- Competitor promise and differentiation notes under [[Competitors]].
- Support workflow patterns under [[Customer Pain Points]].
- Content opportunities under [[Content Engine Home]].

## Open Questions

- Which support workflow has the highest pain and lowest setup burden?
- Is the first product an answer engine, audit tool, support QA layer, or content engine?
- Which integrations are required before a user trusts the product?
"""


B221_HOME_BLOCK = """## Public Workbench Snapshot

### Product Thesis

221B should explore source-grounded AI search and verification workflows: retrieval, citation parsing, evidence scoring, contradiction checks, and repeatable research reports.

### AI Search

- Separate search, retrieval, synthesis, and verification steps.
- Treat citations as claims that need validation, not decoration.
- Keep source quality and answer confidence visible.

### Verification

- Check whether a cited source actually supports the sentence attached to it.
- Distinguish source existence, source relevance, and claim support.
- Track unsupported claims and stale sources as first-class failure cases.

### Citation

- Prefer primary sources where possible.
- Record citation intent: evidence, definition, example, counterpoint, or background.
- Flag claims that rely on inaccessible, low-quality, or circular citations.

### Product Experiments

- Citation verifier for AI-generated research reports.
- Research workflow that produces claim tables before narrative prose.
- Source audit tool for SEO/content pages.
- "Answer with evidence ledger" workflow for founder decisions.

### AI Prompts

- Convert this research answer into claims, evidence, citation quality, and open questions.
- Identify which citations do not support their attached claims.
- Generate a verification plan before writing the final answer.
"""


B221_RESEARCH_BRIEF = """# 221B Public Research Brief

## Working Question

How should a reliable AI research workflow separate answer generation from evidence verification?

## Research Buckets

- RAG evaluation and retrieval quality.
- Citation attribution and citation faithfulness.
- Web search tool design and source constraints.
- Deep research workflows, claim extraction, and evaluation.

## Product Notes

- The product should make uncertainty visible.
- The workflow should produce intermediate artifacts: source list, claim table, contradiction list, and final answer.
- The user should be able to audit why a source was used.

## Open Questions

- Is the highest value in search, verification, citation repair, or report generation?
- What is the minimum useful evidence ledger?
- Which workflow should be a Codex/Claude prompt and which should be productized?
"""


CONTENT_ENGINE_BLOCK = """## Public Workbench Snapshot

### Content Clusters

- DocMind: Shopify customer support automation, AI helpdesk workflows, support QA, customer pain extraction.
- 221B: AI search, citation verification, RAG evaluation, source-grounded research.
- FounderOS: Obsidian AI context vault, Codex workflows, reusable context packs.

### Operating Rule

Every content idea should point back to a source note, a project assumption, a customer pain, or a decision. Avoid generic articles that do not improve product learning.

### Brief Pipeline

1. Source note.
2. Claim/evidence extraction.
3. Search intent and ICP mapping.
4. Outline with internal links.
5. Draft.
6. Repurpose into founder update, X/LinkedIn post, and product insight.

### AI Prompts

- Turn recent source notes into five pain-led content briefs.
- Identify which content ideas support DocMind positioning.
- Build an internal link map for the Shopify support automation cluster.
"""


CONTENT_OPERATING_SYSTEM = """# Public Content Operating System

## Priority Content Lanes

### DocMind

- "How to reduce repetitive Shopify support tickets without replacing your helpdesk."
- "AI support answers need citations: a practical merchant workflow."
- "Turn Shopify support tickets into help center and SEO opportunities."

### 221B

- "Citation is not verification: how to audit AI research answers."
- "A practical evidence ledger for AI search workflows."
- "RAG evaluation for founders: what to check before trusting an answer."

### FounderOS

- "How to build an AI-ready Obsidian context vault."
- "Context packs for Codex, Claude, and ChatGPT: a founder workflow."

## Publishing Checklist

- Source notes linked.
- Project assumption linked.
- Search intent named.
- Internal links selected.
- CTA tied to product learning.
- Repurposing plan included.
"""


AI_WORKFLOW_BLOCK = """## Public Workbench Snapshot

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
"""


AI_WORKFLOW_OPERATING_SYSTEM = """# Public AI Workflow Operating System

## Core Workflows

### Codex Implementation Loop

Use when changing files in this vault or builder. Inputs: goal, affected paths, safety boundary. Output: code/content changes plus verification evidence.

### Source-Grounded Research Loop

Use when adding public research. Inputs: URL list and topic. Output: source notes, manual review list, project links, and open questions.

### Product Strategy Extraction

Use when turning source notes into project decisions. Output: assumptions, evidence, risks, roadmap candidates, and experiments.

### Content Brief Generation

Use when turning research into SEO/content. Output: search intent, audience, outline, source notes, internal links, and CTA.

## Prompt Template

Given this context pack and the linked source notes, produce:
- stable facts
- assumptions
- evidence
- contradictions
- next actions
- questions that need human judgment
"""


RESEARCH_MAP_BLOCK = """## Public Workbench Snapshot

### Current Research Lanes

- AI search and answer quality.
- RAG evaluation and retrieval faithfulness.
- Citation optimization and source attribution.
- Shopify customer support automation.
- FounderOS / Obsidian as an AI-ready operating layer.

### Source Handling

- Public web pages become source notes under [[Source Index]].
- Low-confidence or blocked pages stay in [[MANUAL_REVIEW]].
- Private/local sources remain disabled until a separate plan is approved.

### AI Prompts

- Extract claims and evidence from recent source notes.
- Identify research lanes with too little source support.
- Turn the research map into next week's reading plan.
"""


PUBLIC_SOURCE_MAP = """# Public Source Map

## Purpose

This map tracks public sources that can safely support FounderOS without scanning private files.

## Source Categories

- Obsidian system design: Bases, properties, templates.
- AI workflows: prompt engineering, agent patterns, Codex/Claude workflows.
- Research quality: RAG, citations, verification, web search.
- DocMind market context: Shopify customer support, helpdesk apps, support automation.
- Content and SEO: Google Search Central guidance and topic clusters.

## Current Safety Boundary

- Network metadata and public URL source notes are allowed.
- Online AI, OCR, transcription, embeddings, email, browser sessions, and private folders are not enabled.

## Maintenance

- Add public URLs to `obsidian-vault-builder/data/urls.txt`.
- Run scan, privacy review, import plan, and confirmed import.
- Keep blocked pages in `_System/MANUAL_REVIEW.md`.
"""


DOCMIND_CONTEXT_BLOCK = """## Copy-Ready Context

Use this when asking an AI tool to help with DocMind strategy, SEO, product planning, or support automation.

DocMind is being explored as a Shopify support automation product. The current working thesis is that small ecommerce teams need source-grounded answers, support workflow automation, and a way to turn repeated customer questions into better help docs, product decisions, and content. The product should avoid generic chatbot positioning and emphasize trust, citations, escalation, and low setup burden.

Current assumptions:
- The strongest initial ICP is Shopify merchants or operators with repeated support tickets and thin support capacity.
- The clearest pain areas are repetitive questions, inconsistent policy answers, stale help content, and weak feedback loops from support into growth/product work.
- A strong wedge may be an AI layer that works with existing helpdesk workflows rather than replacing the helpdesk.

When helping, produce practical outputs: ICP assumptions, pain-led SEO briefs, support workflow maps, sales objections, roadmap candidates, and experiment plans. Keep claims tied to source notes or mark them as assumptions.
"""


B221_CONTEXT_BLOCK = """## Copy-Ready Context

Use this when asking an AI tool to help with 221B, AI search, citation quality, source verification, or research workflow design.

221B is an AI search and verification research/product direction. The current working thesis is that useful AI research needs a visible evidence layer: sources, claims, citation support, contradictions, confidence, and open questions. Treat citations as objects to verify, not proof by themselves.

Current assumptions:
- The highest-value workflow separates retrieval, synthesis, and verification.
- A good answer should include an evidence ledger before or alongside prose.
- Product experiments should focus on citation faithfulness, claim support, and auditability.

When helping, produce claim tables, source quality notes, verification plans, contradiction checks, and product experiment ideas.
"""


CONTENT_CONTEXT_BLOCK = """## Copy-Ready Context

Use this when generating SEO briefs, articles, founder updates, or social posts from the vault.

The content engine should serve product learning first. Priority lanes are DocMind Shopify support automation, 221B AI search/verification, and FounderOS AI context workflows. Every content output should link to source notes, project assumptions, customer pains, or decisions.

When helping, produce:
- target reader and search intent
- angle
- outline
- source notes to cite
- internal links
- CTA tied to product learning
- repurposing plan
"""


AI_WORKFLOW_CONTEXT_BLOCK = """## Copy-Ready Context

Use this when designing or executing reusable AI workflows.

The operating style is privacy-first, local-first, and evidence-driven. Risky actions need dry-run, scope, write paths, network/upload statement, and rollback. Codex workflows should inspect existing files, write focused tests where behavior changes, implement narrowly, and verify before reporting completion.

Core reusable workflows:
- Codex implementation loop.
- Public source research loop.
- Product strategy extraction.
- Content brief generation.
- Context pack refresh.

When helping, produce structured steps, inputs, outputs, failure cases, and verification checks.
"""


CURRENT_PROJECTS_CONTEXT_BLOCK = """## Copy-Ready Context

Current focus areas:
- DocMind: Shopify support automation, source-grounded answers, support-to-growth workflows.
- 221B: AI search, citation verification, research quality, evidence ledgers.
- Content Engine: SEO briefs and founder content grounded in source notes.
- FounderOS: Obsidian vault as an AI-ready context layer.

When helping, ask which project is primary only if the requested output depends on it. Otherwise infer from the note, source, or target audience and mark assumptions explicitly.
"""


RESEARCH_CONTEXT_BLOCK = """## Copy-Ready Context

The research system prioritizes public, auditable sources and keeps private/local data disabled unless explicitly approved. Current lanes are AI search, RAG evaluation, citation verification, Shopify support automation, SaaS/customer support, and Obsidian-based AI context management.

When helping with research:
- separate claims from evidence
- prefer primary sources
- identify unsupported claims
- maintain open questions
- turn useful findings into project notes, decision notes, or content briefs
"""
