from __future__ import annotations

from pathlib import Path

from .config import BuilderConfig
from .sanitize import safe_join


MANAGED_MARKER_START = "<!-- founderos-gtm-panel:start -->"
MANAGED_MARKER_END = "<!-- founderos-gtm-panel:end -->"


def write_gtm_operating_panel(config: BuilderConfig) -> list[Path]:
    written: list[Path] = []
    for relative_path, body in gtm_notes().items():
        path = safe_join(config.vault_path, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {Path(relative_path).stem}\n"
        updated = _upsert(existing, body)
        if updated != existing:
            path.write_text(updated, encoding="utf-8")
            written.append(path)
    return written


def gtm_notes() -> dict[str, str]:
    return {
        "Home.md": HOME_GTM_BLOCK,
        "10 Projects/DocMind/DocMind Home.md": DOCMIND_HOME_GTM_BLOCK,
        "10 Projects/DocMind/DocMind GTM Dashboard.md": GTM_DASHBOARD,
        "10 Projects/DocMind/DocMind Daily Operating Rhythm.md": DAILY_OPERATING_RHYTHM,
        "30 Content/DocMind Publish Queue.md": PUBLISH_QUEUE,
        "40 Meetings & People/Customer Calls/DocMind Customer Interview Log.md": CUSTOMER_INTERVIEW_LOG,
        "40 Meetings & People/Customer Calls/DocMind Customer Interview Template.md": CUSTOMER_INTERVIEW_TEMPLATE,
        "40 Meetings & People/People/DocMind Lead Follow-Up Tracker.md": LEAD_FOLLOW_UP_TRACKER,
        "_Templates/DocMind Customer Interview Template.md": CUSTOMER_INTERVIEW_TEMPLATE,
        "_Templates/DocMind Lead Follow-Up Template.md": LEAD_FOLLOW_UP_TEMPLATE,
        "_Context Packs/docmind-gtm-context.md": GTM_CONTEXT,
        "80 Databases/DocMind GTM.base": GTM_BASE,
    }


def _upsert(existing: str, body: str) -> str:
    block = f"{MANAGED_MARKER_START}\n{body.rstrip()}\n{MANAGED_MARKER_END}\n"
    if MANAGED_MARKER_START in existing and MANAGED_MARKER_END in existing:
        start = existing.index(MANAGED_MARKER_START)
        end = existing.index(MANAGED_MARKER_END, start) + len(MANAGED_MARKER_END)
        return f"{existing[:start]}{block.rstrip()}{existing[end:]}".rstrip() + "\n"
    return f"{existing.rstrip()}\n\n{block}"


HOME_GTM_BLOCK = """## DocMind GTM Panel

- [[DocMind GTM Dashboard]]
- [[DocMind Daily Operating Rhythm]]
- [[DocMind Publish Queue]]
- [[DocMind Customer Interview Log]]
- [[DocMind Lead Follow-Up Tracker]]
- [[docmind-gtm-context]]

Boundary: this panel is built from public notes and manual operating scaffolds only. It does not require private customer, order, email, chat, cookie, or session data.
"""


DOCMIND_HOME_GTM_BLOCK = """## GTM Operating Panel

### Current Wedge

Source-grounded support automation for Shopify teams, starting with audit, answer quality, order-status questions, returns policy questions, and safe escalation.

### Operating Pages

- [[DocMind GTM Dashboard]]
- [[DocMind Daily Operating Rhythm]]
- [[DocMind Publish Queue]]
- [[DocMind Landing Page Draft]]
- [[DocMind Demo Script]]
- [[Customer Discovery Questionnaire]]
- [[DocMind Customer Interview Log]]
- [[DocMind Lead Follow-Up Tracker]]

### Weekly Target

- 1 landing page iteration
- 2 publishable content drafts
- 5 customer discovery conversations
- 10 outbound lead attempts
- 1 support automation audit offer
"""


GTM_DASHBOARD = """## Purpose

Run DocMind as a weekly founder operating system: ship one clear offer, publish source-grounded content, speak with customers, and turn discovery into product decisions.

## Current Positioning

DocMind helps Shopify teams reduce repeated support questions by turning approved sources into cited answers, confidence levels, and escalation rules. The first offer is a support automation audit, not a full helpdesk replacement.

## This Week

| Workstream | Target | Working note | Status |
| --- | --- | --- | --- |
| Offer | Support automation audit | [[DocMind Landing Page Draft]] | Draft |
| Demo | Order-status plus shipping-address scenario | [[DocMind Demo Script]] | Draft |
| Content | 3 SEO briefs ready for drafting | [[DocMind Publish Queue]] | Planned |
| Discovery | 5 customer conversations | [[DocMind Customer Interview Log]] | Open |
| Pipeline | 10 leads contacted | [[DocMind Lead Follow-Up Tracker]] | Open |

## Scoreboard

| Metric | Target | Actual | Notes |
| --- | ---: | ---: | --- |
| Customer conversations booked | 5 | 0 | Add real entries manually |
| Customer conversations completed | 5 | 0 | Use [[DocMind Customer Interview Template]] |
| Leads contacted | 10 | 0 | Use [[DocMind Lead Follow-Up Tracker]] |
| Drafts published | 2 | 0 | Use [[DocMind Publish Queue]] |
| Audit offers sent | 3 | 0 | Track offer response |
| Paid pilots | 1 | 0 | Keep at zero until evidence exists |

## Daily Review

1. What shipped yesterday?
2. Which lead, customer, or content asset moved forward?
3. Which source gap blocks a trustworthy support answer?
4. What is the smallest visible output to ship today?
5. What should be copied into [[docmind-gtm-context]] before using an AI tool?

## Decision Links

- [[Decision - Support Automation Wedge]]
- [[DocMind 7-Day Execution Plan]]
- [[Shopify Support Automation Brief]]
- [[AI Helpdesk for Shopify Brief]]
- [[Order Status Support Automation Brief]]
- [[Returns Support Automation Brief]]

## Safety Boundary

Do not claim access to live Shopify store, customer, order, helpdesk, email, or chat data unless a separate approved integration/source plan exists.
"""


DAILY_OPERATING_RHYTHM = """## Morning Startup

- [ ] Review [[DocMind GTM Dashboard]].
- [ ] Pick one shipping task, one discovery task, and one content task.
- [ ] Check whether today's work needs only public sources or a separate private-source approval.
- [ ] Copy only the relevant public context into AI tools.

## Daily Shipping Block

Choose one:

- [ ] Improve [[DocMind Landing Page Draft]].
- [ ] Draft one page from [[DocMind Publish Queue]].
- [ ] Tighten [[DocMind Demo Script]] with a clearer objection or proof point.
- [ ] Update [[Decision - Support Automation Wedge]] from new evidence.

## Daily Discovery Block

Choose one:

- [ ] Add 5 candidate leads to [[DocMind Lead Follow-Up Tracker]].
- [ ] Send 3 support-audit outreach messages.
- [ ] Book 1 customer discovery call.
- [ ] Summarize 1 interview in [[DocMind Customer Interview Log]].

## Daily Source-Grounding Block

- [ ] Open [[Source Index]].
- [ ] Link any claim to source notes where possible.
- [ ] Mark unsupported claims as assumptions.
- [ ] Add source gaps to [[DocMind GTM Dashboard]] or [[Open Questions]].

## End-of-Day Close

- [ ] Update scoreboard numbers manually.
- [ ] Move one task to tomorrow.
- [ ] Record one customer insight, content insight, or product risk.
- [ ] Keep paid pilots, revenue, testimonials, and customer claims at zero unless direct evidence exists.
"""


PUBLISH_QUEUE = """## Purpose

Keep DocMind publishing work tied to source notes, search intent, and the current support automation wedge.

## Queue

| Priority | Asset | Type | Search intent | Source notes | Stage | Next action |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | [[DocMind Landing Page Draft]] | Landing page | Support automation audit | [[Shopify Support Automation Brief]], [[AI Agent explained Untitled]] | Draft | Tighten CTA and proof section |
| 2 | [[Order Status Support Automation Brief]] | SEO brief | Reduce WISMO/order tickets | [[Building apps for customer accounts]], [[Customer]] | Brief | Turn into article outline |
| 3 | [[Returns Support Automation Brief]] | SEO brief | Automate returns safely | [[Support your customers]], [[About Flow]] | Brief | Add escalation examples |
| 4 | [[AI Helpdesk for Shopify Brief]] | SEO brief | Evaluate AI helpdesk tools | [[Gorgias- AI, Helpdesk & Chat - Instantly resolve support inquiries and grow your business. - Shopify App Store]] | Brief | Add comparison angle |
| 5 | [[Shopify Support Automation Brief]] | SEO brief | Shopify support automation | [[Support your customers]] | Brief | Convert into cornerstone page |

## Draft Definition

- Clear reader and search intent.
- One product angle.
- Source notes linked.
- Unsupported claims marked as assumptions.
- CTA tied to support automation audit.

## Publish Definition

- Internal links added.
- No unsupported performance claims.
- No fake customer proof.
- Founder voice included where relevant.
- Next conversion action is visible.
"""


CUSTOMER_INTERVIEW_LOG = """## Purpose

Track customer discovery conversations for DocMind without importing email, CRM, chat, or private customer records. Add entries manually.

## Interview Pipeline

| Person | Company | Segment | Status | Main pain | Next step | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Example lead | Example Shopify store | Founder/operator | To contact | Repeated support questions | Send audit offer | Replace manually |

## Completed Interviews

| Date | Person | Segment | Top repeated question | Trust requirement | First workflow candidate | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |

## Synthesis

### Repeated Pains

- 

### Buying Signals

- 

### Red Flags

- 

### Product Implications

- 

### Content Ideas From Calls

- 
"""


CUSTOMER_INTERVIEW_TEMPLATE = """## Customer Interview

### Frontmatter To Fill

- date:
- person:
- company:
- segment:
- source:
- status:
- follow_up_date:

### Context

- How did this person enter the pipeline?
- What store/support context matters?
- Which claim or assumption is this call testing?

### Questions

1. What are the three most repetitive support questions your team handles each week?
2. Which answers feel risky because policies or customer context can change?
3. Where do you currently look for the correct answer?
4. What happens when customers ask about order status, returns, or shipping changes?
5. Which help center pages or policies are outdated or unclear?
6. What would make you trust an AI-generated support answer?
7. Where should AI never answer without human review?
8. What would a useful first automation look like if it only handled one workflow?

### Notes

- 

### Evidence

- Exact phrases:
- Repeated pain:
- Current workaround:
- Existing tools:
- Budget/timing signal:
- Trust requirement:

### Follow-Up

- First workflow candidate:
- Source gaps:
- Content ideas:
- Product risks:
- Next action:
"""


LEAD_FOLLOW_UP_TRACKER = """## Purpose

Track DocMind outreach manually. Do not import inboxes, CRMs, browser sessions, cookies, or private lead databases into this vault without a separate approved source plan.

## Pipeline

| Lead | Company | Segment | Source | Status | Last touch | Next touch | Offer | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example lead | Example Shopify store | Founder/operator | Manual research | Not contacted |  |  | Support automation audit | Replace manually |

## Status Values

- Not contacted
- Contacted
- Replied
- Discovery booked
- Discovery completed
- Audit offered
- Pilot proposed
- Closed won
- Closed lost
- Nurture

## Outreach Angles

### Audit Offer

I am mapping repeated Shopify support questions into source-grounded answers with confidence and escalation rules. I can run a lightweight support automation audit and show the first workflow your store could automate safely.

### Discovery Ask

I am researching how Shopify teams handle repeated support questions. I am looking for 15 minutes to understand where AI support feels useful, risky, or not worth the setup.

## Follow-Up Rules

- Keep claims specific and evidence-based.
- Do not imply DocMind has read private store data.
- Do not promise ticket reduction without a measured baseline.
- Summarize every reply manually in [[DocMind Customer Interview Log]].
"""


LEAD_FOLLOW_UP_TEMPLATE = """## Lead Follow-Up

### Frontmatter To Fill

- company:
- person:
- segment:
- status:
- last_touch:
- next_touch:
- offer:

### Why This Lead

- 

### Hypothesis

- Repeated support pain:
- Trust requirement:
- First workflow likely to matter:

### Outreach Draft

Hi {{name}},

I am mapping repeated Shopify support questions into source-grounded answers with citations, confidence, and escalation rules. I am looking for a few stores where a lightweight support automation audit would be useful before adding another chatbot or helpdesk workflow.

Would a quick audit of your top repeated support questions be useful?

### Touch History

| Date | Channel | Message | Result | Next step |
| --- | --- | --- | --- | --- |

### Notes

- 
"""


GTM_CONTEXT = """## Copy-Ready DocMind GTM Context

Use this when asking Codex, Claude, or ChatGPT to produce DocMind GTM work.

DocMind is positioned as source-grounded support automation for Shopify teams. The current wedge is a support automation audit and answer-quality layer, not a full helpdesk replacement. The strongest first workflows are order-status questions, returns/policy questions, and product/helpdesk questions that need clear escalation.

Current GTM pages:
- [[DocMind GTM Dashboard]]
- [[DocMind Daily Operating Rhythm]]
- [[DocMind Publish Queue]]
- [[DocMind Landing Page Draft]]
- [[DocMind Demo Script]]
- [[Customer Discovery Questionnaire]]
- [[DocMind Customer Interview Log]]
- [[DocMind Lead Follow-Up Tracker]]

Current source-grounded content assets:
- [[Shopify Support Automation Brief]]
- [[AI Helpdesk for Shopify Brief]]
- [[Order Status Support Automation Brief]]
- [[Returns Support Automation Brief]]

GTM operating rules:
- Keep installs, trials, paid pilots, revenue, testimonials, and case studies at zero unless direct evidence exists.
- Do not imply access to private Shopify, customer, order, helpdesk, email, or chat data.
- Mark unsupported claims as assumptions.
- Prefer audit, answer quality, citations, confidence, and escalation over broad AI replacement claims.
- Founder voice should be practical, specific, and evidence-led.

Useful next prompts:

1. Turn [[DocMind Landing Page Draft]] into sharper homepage copy without inventing proof.
2. Turn [[Order Status Support Automation Brief]] into a 1200-word SEO outline with source-grounded sections.
3. Summarize [[DocMind Customer Interview Log]] into buying signals, red flags, and product changes.
4. Draft five outreach messages for Shopify founders using the support automation audit angle.
"""


GTM_BASE = """filters:
  and:
    - file.ext == "md"
    - or:
    - 'file.inFolder("10 Projects/DocMind")'
    - 'file.inFolder("30 Content")'
    - 'file.inFolder("40 Meetings & People/Customer Calls")'
    - 'file.inFolder("40 Meetings & People/People")'
properties:
  file.name:
    displayName: File.Name
  status:
    displayName: Status
  segment:
    displayName: Segment
  company:
    displayName: Company
  next_touch:
    displayName: Next Touch
  follow_up_date:
    displayName: Follow Up Date
  offer:
    displayName: Offer
views:
  - type: table
    name: DocMind GTM
    order:
    - file.name
    - status
    - segment
    - company
    - next_touch
    - follow_up_date
    - offer
"""
