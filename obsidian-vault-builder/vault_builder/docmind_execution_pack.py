from __future__ import annotations

from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-docmind-execution:start -->"
MANAGED_MARKER_END = "<!-- founderos-docmind-execution:end -->"


def write_docmind_execution_pack(config: BuilderConfig) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in execution_notes().items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def execution_notes() -> dict[str, str]:
    return {
        "10 Projects/DocMind/DocMind 7-Day Execution Plan.md": EXECUTION_PLAN,
        "30 Content/SEO Briefs/AI Helpdesk for Shopify Brief.md": AI_HELPDESK_BRIEF,
        "30 Content/SEO Briefs/Order Status Support Automation Brief.md": ORDER_STATUS_BRIEF,
        "30 Content/SEO Briefs/Returns Support Automation Brief.md": RETURNS_BRIEF,
        "30 Content/Drafts/DocMind Landing Page Draft.md": LANDING_PAGE_DRAFT,
        "50 AI Prompts & Workflows/DocMind Demo Workflow.md": DEMO_WORKFLOW,
        "50 AI Prompts & Workflows/DocMind Demo Script.md": DEMO_SCRIPT,
        "10 Projects/DocMind/Customer Discovery Questionnaire.md": CUSTOMER_DISCOVERY,
        "_Context Packs/docmind-execution-context.md": EXECUTION_CONTEXT,
    }


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"


EXECUTION_PLAN = """## Goal

Turn DocMind from research thesis into a concrete one-week execution package: landing page angle, demo workflow, SEO briefs, source-grounded answer format, and validation tasks.

## Day 1 - Define the wedge

- Primary wedge: source-grounded support automation for Shopify merchants.
- Target user: founder/operator or support lead who handles repeated questions with limited support capacity.
- Promise: reduce repeated support work without replacing the existing helpdesk.
- Output: tighten [[Decision - Support Automation Wedge]] and list the first three workflows.

## Day 2 - Build the demo narrative

- Workflow 1: order status and customer account questions.
- Workflow 2: returns or policy questions.
- Workflow 3: product/helpdesk answer with escalation.
- Output: finish [[DocMind Demo Workflow]].

## Day 3 - Prepare landing page content

- Headline: source-grounded support automation for Shopify teams.
- Sections: pain, trust model, demo workflow, use cases, first audit offer.
- Output: draft the first landing page outline from [[Shopify Support Automation Brief]].

## Day 4 - Publishable SEO brief 1

- Brief: [[Order Status Support Automation Brief]].
- Goal: capture order-status and customer-account automation intent.
- Output: outline plus internal links and CTA.

## Day 5 - Publishable SEO brief 2

- Brief: [[Returns Support Automation Brief]].
- Goal: capture returns, policies, and escalation workflow intent.
- Output: outline plus source-grounded answer examples.

## Day 6 - AI/helpdesk positioning

- Brief: [[AI Helpdesk for Shopify Brief]].
- Goal: differentiate DocMind from generic AI chat and full helpdesk replacement.
- Output: comparison angle and objection responses.

## Day 7 - Validation package

- Build a 5-question customer discovery script.
- Build a 1-page support audit offer.
- Update [[docmind-execution-context]] for Codex, Claude, or ChatGPT execution.

## Done Criteria

- One landing page outline exists.
- Three SEO briefs exist.
- One source-grounded demo workflow exists.
- One copy-ready execution context exists.
- No private/local sources were scanned.
"""


AI_HELPDESK_BRIEF = """## SEO Brief

### Working Title

AI helpdesk for Shopify: what to automate before replacing your support stack

### Search Intent

The reader is evaluating AI support/helpdesk options for a Shopify store and wants a practical, low-risk path.

### Audience

Shopify founders, ecommerce operators, support leads, and solo teams.

### Angle

DocMind should be positioned as a source-grounded layer that improves answers and workflows before a merchant changes their full helpdesk stack.

### Outline

1. Why merchants search for AI helpdesk tools.
2. Why replacing a helpdesk is not the first step.
3. The safer first step: source-grounded answers for repeated questions.
4. How citations, approved sources, and escalation reduce AI risk.
5. What to audit before automation: policies, order status, returns, product FAQs.
6. How DocMind can start as an audit and answer-quality layer.

### Source Notes

- [[AI Agent explained Untitled]]
- [[Gorgias- AI, Helpdesk & Chat - Instantly resolve support inquiries and grow your business. - Shopify App Store]]
- [[Sell on Shopify and support with Gorgias' helpdesk]]
- [[Support your customers]]

### CTA

Offer a support automation audit that identifies the first workflow to automate safely.
"""


ORDER_STATUS_BRIEF = """## SEO Brief

### Working Title

Order status support automation for Shopify stores

### Search Intent

The reader wants to reduce order-status tickets and help customers get reliable order/account answers.

### Audience

Shopify operators and support teams handling "where is my order" and customer account questions.

### Angle

Order status support is a strong first workflow because the answers should be predictable, source-based, and easy to escalate when uncertain.

### Outline

1. Why order-status questions create repeated support load.
2. What customer account and order-status surfaces already provide.
3. Where AI support can help and where it should escalate.
4. Source-grounded answer template: answer, source, confidence, escalation.
5. How to measure ticket reduction and answer quality.

### Source Notes

- [[Building apps for customer accounts]]
- [[Customer]]
- [[Support your customers]]

### CTA

Map the store's top order-status questions and create a source-grounded answer set.
"""


RETURNS_BRIEF = """## SEO Brief

### Working Title

Automating Shopify returns support without losing customer trust

### Search Intent

The reader wants to automate returns or policy support while avoiding wrong answers and customer frustration.

### Audience

Shopify founders, support teams, and ecommerce operators.

### Angle

Returns support should be automated only when source policies are explicit, answer confidence is visible, and escalation rules are clear.

### Outline

1. Why returns questions are high-risk support automation.
2. Which source documents must be clean before automation.
3. How to answer with policy citations.
4. When to escalate instead of answer.
5. How to turn repeated return questions into help center improvements.

### Source Notes

- [[About Flow]]
- [[Support your customers]]
- [[AI Agent explained Untitled]]

### CTA

Run a returns-answer audit: source policy, repeated questions, risky edge cases, and escalation rule.
"""


LANDING_PAGE_DRAFT = """## Landing Page Draft

### Hero

Source-grounded support automation for Shopify teams.

Reduce repeated support questions without replacing your helpdesk. DocMind helps you turn approved policies, customer account workflows, and helpdesk knowledge into answers with citations, confidence, and escalation rules.

### Primary CTA

Get a support automation audit.

### Problem

Shopify support work repeats itself:
- customers ask where orders are
- policies are hard to apply consistently
- help center content gets stale
- AI answers feel risky when they cannot show sources
- support data rarely becomes product or content insight

### What DocMind Does

DocMind maps repeated questions to approved source notes, drafts support answers with source references, flags uncertainty, and shows which help docs or workflows need improvement.

### First Workflows

1. Order status and customer account questions.
2. Returns and policy questions.
3. Product/helpdesk questions that need escalation.

### Trust Model

- Approved sources only.
- Cited answer format.
- Confidence level.
- Escalation when source support is missing.
- No private customer/order data in demo mode.

### Audit Offer

The first offer is a lightweight support automation audit:
- top repeated support questions
- source/policy gaps
- risky automation areas
- first workflow to automate safely
- suggested answer format and escalation rules

### Objection Handling

- Already using a helpdesk: DocMind starts as an answer-quality and audit layer.
- Worried about AI mistakes: DocMind shows sources and confidence.
- No time to set up: start with one repeated workflow.
- Policies change often: stale-source detection becomes part of the workflow.
"""


DEMO_WORKFLOW = """## Demo Workflow

### Scenario

A Shopify customer asks: "Where is my order, and can I change my shipping address?"

### Source-grounded answer flow

1. Identify intent: order status plus account/order action.
2. Retrieve approved sources: customer account docs, order status source, merchant policy note.
3. Draft answer with source citations.
4. Check confidence:
   - High: answer directly and cite source.
   - Medium: answer the generic part and ask for needed order/account detail.
   - Low: escalate to human support.
5. Log repeated question and missing source gaps.

### Output Format

- Answer:
- Source used:
- Confidence:
- Escalation needed:
- Follow-up data needed:
- Help center gap:

### Example

Use a source-grounded answer for public/general policy. Do not invent order-specific data unless a private approved integration is available.

### Demo Boundary

This workflow uses public source notes only. Real customer/order data requires a separate approved private-source or API plan.
"""


DEMO_SCRIPT = """## Demo Script

### Setup

Use this as a narrated walkthrough for a DocMind demo. The demo uses public source notes only and does not access real customer or order data.

### Opening

"Most Shopify teams do not need another generic chatbot first. They need a safer way to answer repeated support questions from approved sources, show confidence, and escalate when the source is missing."

### Step 1 - Pick a repeated question

Customer asks: "Where is my order, and can I change my shipping address?"

### Step 2 - Identify intent

- Intent 1: order status.
- Intent 2: account or order action.
- Risk: the system should not invent order-specific facts.

### Step 3 - Retrieve approved sources

Use source notes:
- [[Building apps for customer accounts]]
- [[Customer]]
- [[Support your customers]]

### Step 4 - Draft source-grounded answer

Answer structure:
- what the customer can generally do
- what information is needed
- source used
- confidence level
- escalation rule

### Step 5 - Show safety behavior

If order-specific data is unavailable, the answer should say that a human or approved integration is needed. The demo should make this restraint visible.

### Step 6 - Turn support into improvement

Log:
- repeated question
- missing help center article
- source/policy gap
- candidate automation workflow

### Closing

"DocMind starts with one workflow, proves answer quality, and turns support repetition into better sources, better content, and safer automation."
"""


CUSTOMER_DISCOVERY = """## Customer Discovery

### Target Interviewee

Shopify founder/operator, ecommerce support lead, or small team member handling repeated customer questions.

### Discovery questions

1. What are the three most repetitive support questions your team handles each week?
2. Which support answers feel risky because policies or customer context can change?
3. Where do agents or founders currently look for the correct answer?
4. What happens when a customer asks about order status, returns, or shipping changes?
5. Which help center pages or policies are most often outdated or unclear?
6. What would make you trust an AI-generated support answer?
7. Where should AI never answer without human review?
8. Do you already use Gorgias, Zendesk, Shopify Inbox, or another helpdesk?
9. What would a useful first automation look like if it only handled one workflow?
10. Would a support automation audit be useful before installing any tool?

### Buying Signals

- Repeated questions are handled manually.
- Help center content is stale.
- Existing helpdesk automation feels hard to configure.
- Founder/operator still answers customer tickets.
- Team wants AI but fears wrong answers.

### Red Flags

- No repeated support volume.
- No willingness to organize source docs.
- User wants a fully autonomous chatbot without review or escalation.
- Support data is inaccessible and no integration path exists.

### Follow-up Output

After each interview, create:
- top pain points
- first automation candidate
- trust requirements
- source gaps
- content brief ideas
- product risks
"""


EXECUTION_CONTEXT = """## Copy-Ready DocMind Execution Context

Use this context with Codex, Claude, or ChatGPT when working on the DocMind one-week execution package.

DocMind is currently positioned as source-grounded support automation for Shopify merchants. The first wedge is not replacing the helpdesk. The wedge is improving answer quality, repeated-question workflows, and support-to-content/product feedback loops by using approved sources, citations, confidence, and escalation.

Current execution outputs:
- [[DocMind 7-Day Execution Plan]]
- [[Decision - Support Automation Wedge]]
- [[Shopify Support Automation Brief]]
- [[AI Helpdesk for Shopify Brief]]
- [[Order Status Support Automation Brief]]
- [[Returns Support Automation Brief]]
- [[DocMind Demo Workflow]]
- [[DocMind Demo Script]]
- [[DocMind Landing Page Draft]]
- [[Customer Discovery Questionnaire]]

Useful source clusters:
- Shopify customer accounts and order status: [[Building apps for customer accounts]], [[Customer]]
- Shopify automation/app support: [[About Flow]], [[Support your customers]]
- Helpdesk/AI agent positioning: [[AI Agent explained Untitled]], [[Gorgias- AI, Helpdesk & Chat - Instantly resolve support inquiries and grow your business. - Shopify App Store]], [[Sell on Shopify and support with Gorgias' helpdesk]]

Operating rules:
- Mark unsupported claims as assumptions.
- Do not imply access to private store/customer/order data.
- Keep demo workflows source-grounded.
- Prefer an audit/answer-quality wedge before full automation claims.
"""
