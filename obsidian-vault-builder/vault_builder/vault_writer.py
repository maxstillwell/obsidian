from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .sanitize import safe_join


VAULT_DIRS = [
    "00 Inbox",
    "01 Daily Notes",
    "02 Fleeting Notes",
    "10 Projects/DocMind",
    "10 Projects/221B",
    "10 Projects/Other Projects",
    "20 Research/AI Search",
    "20 Research/RAG",
    "20 Research/Verification",
    "20 Research/Citation Optimization",
    "20 Research/SaaS",
    "20 Research/Shopify",
    "20 Research/Customer Support Automation",
    "20 Research/Papers",
    "20 Research/Articles",
    "20 Research/Notes",
    "30 Content/Topic Ideas",
    "30 Content/SEO Briefs",
    "30 Content/Drafts",
    "30 Content/Published",
    "30 Content/Social Repurposing",
    "30 Content/Source Notes",
    "40 Meetings & People/Meetings",
    "40 Meetings & People/Customer Calls",
    "40 Meetings & People/People",
    "40 Meetings & People/Companies",
    "40 Meetings & People/Investors",
    "40 Meetings & People/Partners",
    "50 AI Prompts & Workflows/Prompt Library",
    "50 AI Prompts & Workflows/Agent Patterns",
    "50 AI Prompts & Workflows/Codex Workflows",
    "50 AI Prompts & Workflows/Claude Code Workflows",
    "50 AI Prompts & Workflows/ChatGPT Workflows",
    "50 AI Prompts & Workflows/Skill Specs",
    "50 AI Prompts & Workflows/Tool Evaluations",
    "50 AI Prompts & Workflows/Automation Ideas",
    "50 AI Prompts & Workflows/Failure Cases",
    "60 Resources/Books",
    "60 Resources/Articles",
    "60 Resources/PDFs",
    "60 Resources/Videos",
    "60 Resources/Courses",
    "60 Resources/Bookmarks",
    "60 Resources/Websites",
    "60 Resources/GitHub Repos",
    "70 Assets/Attachments",
    "70 Assets/Images",
    "70 Assets/Audio",
    "70 Assets/Video",
    "70 Assets/PDFs",
    "70 Assets/Spreadsheets",
    "70 Assets/Presentations",
    "80 Databases",
    "90 Archive",
    "_Context Packs",
    "_Indexes",
    "_Templates",
    "_System",
]


@dataclass
class CreateResult:
    vault_path: Path
    created_dirs: list[Path] = field(default_factory=list)
    created_files: list[Path] = field(default_factory=list)
    skipped_files: list[Path] = field(default_factory=list)


def create_vault(vault_path: Path | str) -> CreateResult:
    root = Path(vault_path).expanduser()
    result = CreateResult(vault_path=root)
    for dirname in VAULT_DIRS:
        path = safe_join(root, dirname)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            result.created_dirs.append(path)
        else:
            path.mkdir(parents=True, exist_ok=True)

    for relative_path, content in build_vault_files().items():
        path = safe_join(root, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            result.skipped_files.append(path)
            continue
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        result.created_files.append(path)
    return result


def build_vault_files() -> dict[str, str]:
    files: dict[str, str] = {}
    files["Home.md"] = HOME
    files.update(home_notes())
    files.update(project_notes())
    files.update(index_notes())
    files.update(template_notes())
    files.update(context_packs())
    files.update(database_base_files())
    files.update(database_setup_notes())
    files.update(system_notes())
    return files


def home_notes() -> dict[str, str]:
    return {
        "00 Inbox/Inbox.md": simple_note("Inbox", ["Capture", "Needs Processing", "Promote To"]),
        "01 Daily Notes/Daily Notes Home.md": simple_note("Daily Notes Home", ["Purpose", "Recent Daily Notes", "Review Prompts"]),
        "02 Fleeting Notes/Fleeting Notes Home.md": simple_note("Fleeting Notes Home", ["Purpose", "Promote Candidates"]),
        "10 Projects/Projects Home.md": simple_note("Projects Home", ["Active Projects", "Open Questions", "Project Review Prompts"]),
        "10 Projects/Other Projects/Other Projects Home.md": simple_note("Other Projects Home", ["Projects", "Parking Lot"]),
        "20 Research/Research Map.md": RESEARCH_MAP,
        "30 Content/Content Engine Home.md": CONTENT_ENGINE_HOME,
        "30 Content/Content Clusters.md": simple_note("Content Clusters", ["Clusters", "Gaps", "Internal Links"]),
        "30 Content/Internal Links Map.md": simple_note("Internal Links Map", ["Core Pages", "Project Links", "Content Links"]),
        "40 Meetings & People/Meetings Home.md": simple_note("Meetings Home", ["Recent Meetings", "Customer Calls", "Follow-ups"]),
        "50 AI Prompts & Workflows/AI Workflow Library.md": AI_WORKFLOW_LIBRARY,
        "60 Resources/Resources Home.md": simple_note("Resources Home", ["Books", "Articles", "PDFs", "Bookmarks", "GitHub Repos"]),
        "80 Databases/Databases Home.md": simple_note("Databases Home", ["Setup Notes", "Frontmatter Fields", "Views"]),
        "90 Archive/Archive Home.md": simple_note("Archive Home", ["Purpose", "Archived Projects", "Archived Resources"]),
    }


def project_notes() -> dict[str, str]:
    docmind = {
        "10 Projects/DocMind/DocMind Home.md": DOCMIND_HOME,
        "10 Projects/DocMind/Product Strategy.md": simple_note("Product Strategy", ["Thesis", "Risks", "Next Questions"]),
        "10 Projects/DocMind/ICP.md": simple_note("ICP", ["Segments", "Evidence", "Open Questions"]),
        "10 Projects/DocMind/Customer Pain Points.md": simple_note("Customer Pain Points", ["Pain Points", "Evidence", "SEO Angles"]),
        "10 Projects/DocMind/SEO Strategy.md": simple_note("SEO Strategy", ["Clusters", "Pages", "Internal Links"]),
        "10 Projects/DocMind/Growth Experiments.md": simple_note("Growth Experiments", ["Ideas", "Hypotheses", "Results"]),
        "10 Projects/DocMind/Sales Objections.md": simple_note("Sales Objections", ["Objections", "Responses", "Evidence"]),
        "10 Projects/DocMind/Competitors.md": simple_note("Competitors", ["Competitors", "Positioning", "Gaps"]),
        "10 Projects/DocMind/Roadmap.md": simple_note("Roadmap", ["Now", "Next", "Later"]),
        "10 Projects/DocMind/Open Questions.md": simple_note("Open Questions", ["Product", "Market", "Growth"]),
    }
    b221 = {
        "10 Projects/221B/221B Home.md": B221_HOME,
        "10 Projects/221B/AI Search.md": simple_note("AI Search", ["Thesis", "Workflows", "Open Questions"]),
        "10 Projects/221B/Verification.md": simple_note("Verification", ["Methods", "Failure Modes", "Experiments"]),
        "10 Projects/221B/Citation.md": simple_note("Citation", ["Citation Quality", "Source Reliability", "Experiments"]),
        "10 Projects/221B/Research Workflow.md": simple_note("Research Workflow", ["Capture", "Verify", "Synthesize"]),
        "10 Projects/221B/Product Experiments.md": simple_note("Product Experiments", ["Ideas", "Test Design", "Results"]),
        "10 Projects/221B/Open Questions.md": simple_note("Open Questions", ["Research", "Product", "Market"]),
    }
    return {**docmind, **b221}


def index_notes() -> dict[str, str]:
    titles = [
        "Master Index",
        "Project Index",
        "DocMind Index",
        "221B Index",
        "Content Index",
        "Research Index",
        "Meeting Index",
        "People Index",
        "Decision Index",
        "Source Index",
        "AI Workflow Index",
        "Tag Index",
    ]
    return {f"_Indexes/{title}.md": index_note(title) for title in titles}


def template_notes() -> dict[str, str]:
    return {
        "_Templates/Daily Note Template.md": DAILY_TEMPLATE,
        "_Templates/Project Template.md": PROJECT_TEMPLATE,
        "_Templates/Meeting Template.md": MEETING_TEMPLATE,
        "_Templates/Customer Call Template.md": CUSTOMER_CALL_TEMPLATE,
        "_Templates/Research Note Template.md": RESEARCH_TEMPLATE,
        "_Templates/Content Brief Template.md": CONTENT_TEMPLATE,
        "_Templates/Decision Template.md": DECISION_TEMPLATE,
        "_Templates/Source Note Template.md": SOURCE_TEMPLATE,
        "_Templates/Person Template.md": PERSON_TEMPLATE,
        "_Templates/Company Template.md": COMPANY_TEMPLATE,
        "_Templates/Prompt Template.md": PROMPT_TEMPLATE,
        "_Templates/AI Workflow Template.md": AI_WORKFLOW_TEMPLATE,
        "_Templates/Book Note Template.md": simple_template("book", "Book Note", ["Bibliographic Info", "Summary", "Highlights", "Implications", "Related Notes"]),
        "_Templates/Article Note Template.md": simple_template("article", "Article Note", ["Source", "Summary", "Claims", "Evidence", "Implications", "Related Notes"]),
        "_Templates/Weekly Review Template.md": WEEKLY_TEMPLATE,
        "_Templates/Monthly Review Template.md": MONTHLY_TEMPLATE,
    }


def context_packs() -> dict[str, str]:
    return {
        "_Context Packs/founder-profile-context.md": FOUNDER_CONTEXT,
        "_Context Packs/docmind-context.md": DOCMIND_CONTEXT,
        "_Context Packs/221b-context.md": B221_CONTEXT,
        "_Context Packs/content-strategy-context.md": CONTENT_CONTEXT,
        "_Context Packs/ai-workflow-context.md": AI_WORKFLOW_CONTEXT,
        "_Context Packs/research-context.md": RESEARCH_CONTEXT,
        "_Context Packs/current-projects-context.md": CURRENT_PROJECTS_CONTEXT,
        "_Context Packs/weekly-review-context.md": simple_note("Weekly Review Context", ["Purpose", "Inputs", "Review Prompt"]),
    }


def database_setup_notes() -> dict[str, str]:
    specs = {
        "Projects": ["project", "status", "area", "current_focus", "next_actions", "confidence"],
        "Content": ["status", "target_keyword", "product", "funnel_stage", "persona", "source_notes"],
        "Meetings": ["date", "project", "people", "company", "status"],
        "Research": ["topic", "source", "author", "date", "confidence", "status"],
        "People": ["name", "company", "role", "relationship", "projects", "last_contact"],
        "Decisions": ["date", "project", "status", "confidence", "review_date", "outcome"],
        "Sources": ["source_type", "source_path", "source_url", "imported_at", "project", "area", "pii_level", "hash"],
    }
    return {f"80 Databases/{name} Database Setup.md": database_note(name, fields) for name, fields in specs.items()}


def database_base_files() -> dict[str, str]:
    specs = {
        "Projects": {
            "filters": ['type == "project"', 'file.inFolder("10 Projects")'],
            "order": ["file.name", "status", "area", "current_focus", "next_actions", "confidence"],
        },
        "Content": {
            "filters": ['type == "content"', 'file.inFolder("30 Content")'],
            "order": ["file.name", "status", "target_keyword", "product", "funnel_stage", "persona"],
        },
        "Meetings": {
            "filters": ['type == "meeting"', 'type == "customer_call"', 'file.inFolder("40 Meetings & People")'],
            "order": ["file.name", "date", "project", "people", "company", "status"],
        },
        "Research": {
            "filters": ['type == "research"', 'file.inFolder("20 Research")'],
            "order": ["file.name", "topic", "source", "author", "date", "confidence", "status"],
        },
        "People": {
            "filters": ['type == "person"', 'type == "company"', 'file.inFolder("40 Meetings & People/People")'],
            "order": ["file.name", "name", "company", "role", "relationship", "projects", "last_contact"],
        },
        "Decisions": {
            "filters": ['type == "decision"', 'file.hasTag("decision")'],
            "order": ["file.name", "date", "project", "status", "confidence", "review_date"],
        },
        "Sources": {
            "filters": ['type == "source"', 'file.inFolder("60 Resources")'],
            "order": ["file.name", "source_type", "source_url", "imported_at", "project", "area", "pii_level"],
        },
    }
    return {f"80 Databases/{name}.base": base_file(name, spec["filters"], spec["order"]) for name, spec in specs.items()}


def system_notes() -> dict[str, str]:
    now = datetime.now().isoformat(timespec="seconds")
    return {
        "_System/README.md": SYSTEM_README,
        "_System/IMPORT_PLAN.md": IMPORT_PLAN,
        "_System/SCAN_REPORT.md": empty_report("SCAN_REPORT", "No scan has been run. Gate A is still pending."),
        "_System/PRIVACY_REVIEW.md": empty_report("PRIVACY_REVIEW", "No privacy review has been run. Gate A is still pending."),
        "_System/CHANGELOG.md": f"# CHANGELOG\n\n## {now}\n\n- Created first-round FounderOS vault scaffold.\n- Created templates, indexes, context packs, database setup notes, and system reports.\n- No personal source directories were scanned.\n- Next step: confirm `obsidian-vault-builder/config/sources.yaml`.\n",
        "_System/IMPORT_LOG.md": empty_report("IMPORT_LOG", "No imports have been executed."),
        "_System/ERROR_LOG.md": empty_report("ERROR_LOG", "No errors recorded by the vault scaffold."),
        "_System/MANUAL_REVIEW.md": empty_report("MANUAL_REVIEW", "No scan has been run, so no manual review queue exists yet."),
        "_System/DEDUPE_REPORT.md": empty_report("DEDUPE_REPORT", "No dedupe pass has been run."),
        "_System/GATE_STATUS.md": empty_report("GATE_STATUS", "Gate status has not been generated yet."),
        "_System/SOURCES.md": SOURCES_DOC,
        "_System/RULES.md": RULES_DOC,
    }


def simple_note(title: str, sections: list[str]) -> str:
    body = "\n\n".join(f"## {section}\n" for section in sections)
    return f"# {title}\n\n{body}"


def simple_template(note_type: str, title: str, sections: list[str]) -> str:
    body = "\n\n".join(f"## {section}\n" for section in sections)
    return f"---\ntype: {note_type}\ntags:\n  - {note_type}\n---\n\n# {title}\n\n{body}"


def index_note(title: str) -> str:
    return simple_note(title, ["Purpose", "Key Areas", "Recent Imports", "High-Value Notes", "Needs Review", "Open Questions", "Related Projects", "AI Prompts"])


def database_note(name: str, fields: list[str]) -> str:
    fields_md = "\n".join(f"- `{field}`" for field in fields)
    return f"""# {name} Database Setup

## Purpose

Use this setup note to create an Obsidian Bases view when the local Bases format is confirmed.

## Filter

- Include notes where `type` or folder location matches `{name.lower()}`.

## Display Fields

{fields_md}

## Sort

- Most recently modified or most recent `date` first.

## Use

- Review, filter, and maintain {name.lower()} records without importing raw source files directly.
"""


def base_file(name: str, filters: list[str], order: list[str]) -> str:
    filter_lines = "\n".join(f'    - \'{item}\'' for item in filters)
    property_lines = "\n".join(f"  {field}:\n    displayName: {field.replace('_', ' ').title()}" for field in order)
    order_lines = "\n".join(f"    - {field}" for field in order)
    return f"""filters:
  and:
    - file.ext == "md"
    - or:
{filter_lines}
properties:
{property_lines}
views:
  - type: table
    name: {name}
    order:
{order_lines}
"""


def empty_report(title: str, message: str) -> str:
    return f"# {title}\n\n## Status\n\n{message}\n\n## Next Step\n\nConfirm `sources.yaml` before running any scan.\n"


HOME = """# FounderOS

## Current Focus
- [[DocMind Home]]
- [[221B Home]]
- [[Content Engine Home]]
- [[AI Workflow Library]]
- [[Research Map]]

## Dashboards
- [[Master Index]]
- [[Project Index]]
- [[Content Index]]
- [[Research Index]]
- [[Meeting Index]]
- [[Decision Index]]
- [[Source Index]]

## Core Context Packs
- [[founder-profile-context]]
- [[docmind-context]]
- [[221b-context]]
- [[content-strategy-context]]
- [[ai-workflow-context]]
- [[research-context]]

## Daily / Weekly
- [[Daily Notes Home]]
- [[Weekly Review Template]]
- [[Monthly Review Template]]

## Open Questions
- What is the highest leverage thing to work on this week?
- Which ideas have evidence?
- Which projects are under-defined?
- Which notes should become content?
- Which customer pains appear repeatedly?
- Which assumptions need validation?

## AI Prompts
- Summarize my current strategic focus from this vault.
- Find contradictions across my project notes.
- Extract the top customer pain points from recent meetings.
- Turn recent research notes into content briefs.
- Generate next week's founder review from recent notes.
- Build a context pack for a specific project.
"""

DOCMIND_HOME = simple_note("DocMind Home", ["Product Thesis", "ICP", "Customer Pain Points", "SEO Strategy", "Growth Experiments", "Sales Objections", "Competitors", "Roadmap", "Decision Log", "Open Questions", "Related Notes", "AI Prompts"])
B221_HOME = simple_note("221B Home", ["Product Thesis", "AI Search", "Verification", "Citation", "Research Workflow", "Experiments", "Open Questions", "Related Notes", "AI Prompts"])
CONTENT_ENGINE_HOME = simple_note("Content Engine Home", ["Content Clusters", "SEO Briefs", "Drafts", "Published", "Social Repurposing", "Source Notes", "Internal Links", "CTA Library", "AI Prompts"])
AI_WORKFLOW_LIBRARY = simple_note("AI Workflow Library", ["Prompt Library", "Agent Patterns", "Codex Workflows", "Claude Code Workflows", "ChatGPT Workflows", "Skill Specs", "Automation Ideas", "Failure Cases", "AI Prompts"])
RESEARCH_MAP = simple_note("Research Map", ["AI Search", "RAG", "Verification", "Citation Optimization", "SaaS", "Shopify", "Customer Support Automation", "Papers", "Articles", "Open Questions", "AI Prompts"])

DAILY_TEMPLATE = """---
type: daily
date: {{date}}
focus:
projects:
meetings:
ideas:
decisions:
links:
tags:
  - daily
---

# {{date}}

## Focus

## Capture

## Meetings

## Ideas

## Decisions

## Project Updates

## Content Ideas

## Research Notes

## Links

## Tasks

## AI End-of-Day Review
- What were the most important insights today?
- Which notes should be promoted into project notes?
- Which ideas should become content?
- Which assumptions need validation?
- What should I focus on tomorrow?
"""

PROJECT_TEMPLATE = """---
type: project
project:
status:
area:
owner:
start_date:
related_people:
related_notes:
current_focus:
open_questions:
next_actions:
tags:
  - project
---

# Project Name

## Thesis

## Current Focus

## Problem

## Target Users

## Strategy

## Roadmap

## Decisions

## Open Questions

## Next Actions

## Related Notes

## AI Prompts
- Summarize the current state of this project.
- Identify unclear assumptions.
- Extract possible growth experiments.
- Generate next actions.
"""

MEETING_TEMPLATE = """---
type: meeting
date:
project:
people:
company:
source:
status:
tags:
  - meeting
---

# Meeting Title

## Summary

## Decisions

## Customer Pain Points

## Objections

## Opportunities

## Follow-up Actions

## Raw Notes

## Links

## AI Prompts
- Extract product insights.
- Extract customer pain points.
- Extract objections and buying signals.
- Convert this meeting into next actions.
- Link this meeting to relevant project notes.
"""

CUSTOMER_CALL_TEMPLATE = """---
type: customer_call
date:
project:
customer:
company:
role:
industry:
source:
status:
tags:
  - customer-call
---

# Customer Call

## Context

## Customer Profile

## Current Workflow

## Pain Points

## Objections

## Feature Requests

## Buying Signals

## Quotes

## Follow-up Actions

## Product Implications

## Related Notes
"""

RESEARCH_TEMPLATE = """---
type: research
topic:
source:
author:
date:
status:
confidence:
tags:
  - research
---

# Research Note

## Claim

## Evidence

## Counterpoints

## Implications

## Related Notes

## Questions

## AI Prompts
- Summarize this research for product strategy.
- Extract claims and evidence.
- Find related notes.
- Turn this into a content brief.
"""

CONTENT_TEMPLATE = """---
type: content
status:
target_keyword:
product:
funnel_stage:
persona:
source_notes:
tags:
  - content
---

# Content Brief

## Search Intent

## Audience

## Angle

## Outline

## Supporting Notes

## Internal Links

## CTA

## Draft Notes

## Repurposing Ideas

## AI Prompts
- Generate a draft from this brief.
- Improve this for search intent.
- Create LinkedIn and X versions.
- Suggest internal links.
"""

DECISION_TEMPLATE = """---
type: decision
date:
project:
status:
confidence:
review_date:
tags:
  - decision
---

# Decision

## Decision

## Context

## Alternatives

## Reasoning

## Risks

## Expected Outcome

## Review Date

## Actual Outcome

## Related Notes
"""

SOURCE_TEMPLATE = """---
type: source
title:
created:
modified:
imported_at:
source_path:
source_url:
source_type:
project:
area:
tags:
related:
status:
confidence:
pii_level:
hash:
---

# Source Note

## Summary

## Key Points

## Why This Matters

## Related Projects

## Related Notes

## Original Reference

## Import Metadata
"""

PERSON_TEMPLATE = """---
type: person
name:
company:
role:
relationship:
projects:
last_contact:
tags:
  - person
---

# Person Name

## Context

## Relationship

## Projects

## Notes

## Meetings

## Follow-up

## Related Notes
"""

COMPANY_TEMPLATE = """---
type: company
company:
industry:
relationship:
projects:
tags:
  - company
---

# Company Name

## Context

## Relationship

## People

## Meetings

## Opportunities

## Related Notes
"""

PROMPT_TEMPLATE = """---
type: prompt
tool:
use_case:
status:
tags:
  - prompt
---

# Prompt

## Use Case

## Prompt

## Inputs

## Output Format

## Notes

## Failure Modes

## Related Workflows
"""

AI_WORKFLOW_TEMPLATE = """---
type: ai_workflow
tools:
status:
area:
tags:
  - ai-workflow
---

# AI Workflow

## Goal

## Inputs

## Steps

## Tools

## Output

## Evaluation

## Failure Modes

## Improvements
"""

WEEKLY_TEMPLATE = """---
type: weekly_review
week:
date:
tags:
  - weekly-review
---

# Weekly Review

## Highlights

## Product Insights

## Customer Insights

## Content Opportunities

## Research Insights

## Decisions

## Risks

## Next Week Focus

## AI Review Prompts
- Summarize this week across daily notes.
- Extract repeated themes.
- Identify unresolved decisions.
- Generate next week priorities.
"""

MONTHLY_TEMPLATE = """---
type: monthly_review
month:
date:
tags:
  - monthly-review
---

# Monthly Review

## Summary

## Projects

## Content

## Research

## Meetings

## Decisions

## Wins

## Bottlenecks

## Strategic Adjustments

## Next Month Focus
"""

FOUNDER_CONTEXT = """# Founder Profile Context

## Who I Am
- 我是一个关注 AI 产品、创业、增长、SEO、知识系统和自动化工作流的人。
- 我的工作方式偏向系统化、长期沉淀、反复复用上下文。
- 我希望 AI 不只是回答问题，而是帮我构建 workflow、判断优先级、总结模式、复用知识。

## Main Projects
- [[DocMind Home]]
- [[221B Home]]
- [[Content Engine Home]]
- [[AI Workflow Library]]

## Strategic Themes
- AI products
- AI customer support
- AI search
- verification
- citation optimization
- SEO
- content engine
- agent workflows
- personal knowledge management
- founder operating system

## Preferences
- Prefer structured outputs.
- Prefer actionable recommendations.
- Prefer preserving context.
- Prefer linking ideas across projects.
- Prefer privacy-first workflows.
- Prefer local-first knowledge base.

## Reusable AI Instructions
- Use my vault context before giving generic advice.
- Link suggestions to projects, decisions, and notes.
- Separate facts, assumptions, and recommendations.
- Identify open questions and next actions.
- Avoid over-organizing low-value material.
"""

DOCMIND_CONTEXT = """# DocMind Context

## What DocMind Is

DocMind is one of my core projects. It relates to AI customer support, product strategy, Shopify/SaaS merchants, knowledge automation, SEO, and growth experiments.

## Core Areas
- [[ICP]]
- [[Customer Pain Points]]
- [[SEO Strategy]]
- [[Growth Experiments]]
- [[Sales Objections]]
- [[Competitors]]
- [[Roadmap]]

## ICP

## Customer Pain Points

## Product Thesis

## SEO Strategy

## Growth Experiments

## Sales Objections

## Competitors

## Roadmap

## Open Questions

## AI Prompts
- Summarize DocMind's current positioning.
- Extract ICP assumptions.
- Generate growth experiments.
- Turn customer pain points into SEO pages.
- Identify contradictions in strategy.
- Create a product roadmap from current notes.
"""

B221_CONTEXT = """# 221B Context

## What 221B Is

221B is one of my core AI product/research directions. It relates to AI search, verification, citations, research workflow, source reliability, and answer quality.

## Core Areas
- [[AI Search]]
- [[Verification]]
- [[Citation]]
- [[Research Workflow]]
- [[Product Experiments]]

## Product Thesis

## Research Questions

## Verification Ideas

## Citation Ideas

## AI Search Workflows

## Experiments

## Open Questions

## AI Prompts
- Summarize the current 221B thesis.
- Extract product opportunities.
- Identify research gaps.
- Convert research notes into product experiments.
- Compare 221B and DocMind opportunities.
"""

CONTENT_CONTEXT = """# Content Strategy Context

## Content Engine Purpose

This context pack helps generate SEO briefs, articles, social posts, internal links, and content clusters based on my vault.

## Core Areas
- Topic Ideas
- SEO Briefs
- Drafts
- Published
- Social Repurposing
- Source Notes
- Internal Links
- CTA

## Topic Clusters
- AI customer support
- Shopify support automation
- AI search
- verification
- citation optimization
- RAG
- AI workflows
- founder operating system
- Obsidian AI knowledge base

## Target Audiences
- founders
- SaaS operators
- Shopify merchants
- product builders
- growth marketers
- AI power users

## Reusable AI Prompts
- Generate SEO brief from source notes.
- Turn research into blog outline.
- Repurpose article into LinkedIn, X, newsletter.
- Suggest internal links.
- Identify content gaps.
- Map content to funnel stage.
"""

AI_WORKFLOW_CONTEXT = """# AI Workflow Context

## Purpose

This context pack captures my reusable AI workflows, prompts, agent patterns, Codex workflows, Claude Code workflows, skill specs, tool evaluations, and failure cases.

## Core Areas
- Prompt Library
- Agent Patterns
- Codex Workflows
- Claude Code Workflows
- ChatGPT Workflows
- Skill Specs
- Tool Evaluations
- Automation Ideas
- Failure Cases

## Principles
- Preserve context.
- Make workflows reusable.
- Prefer structured input and output.
- Separate planning, execution, review.
- Use dry-runs for risky automation.
- Keep privacy boundaries explicit.

## Reusable AI Prompts
- Design a workflow from this goal.
- Turn this repeated task into an AI skill.
- Write a Codex prompt for this automation.
- Evaluate failure modes.
- Create test cases for this workflow.
- Convert notes into a reusable playbook.
"""

RESEARCH_CONTEXT = """# Research Context

## Core Themes
- AI Search
- RAG
- Verification
- Citation Optimization
- SaaS
- Shopify
- Customer Support Automation
- AI Agents
- Knowledge Management

## Research Workflow
1. Capture source.
2. Extract claims.
3. Record evidence.
4. Add counterpoints.
5. Link implications to projects.
6. Convert useful insights into decisions, experiments, or content.

## AI Prompts
- Extract claims and evidence.
- Find contradictions.
- Summarize implications for DocMind.
- Summarize implications for 221B.
- Generate content ideas.
- Generate product experiments.
"""

CURRENT_PROJECTS_CONTEXT = """# Current Projects Context

## Active Projects
- DocMind
- 221B
- Content Engine
- AI Workflow Library
- FounderOS Vault

## Project Review Prompt

When using this context, help me:
- identify the highest leverage project
- clarify open questions
- extract next actions
- connect research to product
- turn meetings into decisions
- turn ideas into experiments
"""

SYSTEM_README = """# FounderOS System README

## Vault Structure

This vault is a Founder OS + AI Context Vault. It stores project notes, research maps, content workflows, meeting records, resources, context packs, indexes, templates, and system reports.

## Privacy Principles

- Preserve originals.
- Use dry-run before scan or import.
- Do not read sensitive files by default.
- Do not scan broad folders until `sources.yaml` is confirmed.
- Do not use network, online AI, OCR, transcription, email, chats, cookies, or browser sessions without explicit approval.

## Import Flow

1. Confirm `obsidian-vault-builder/config/sources.yaml`.
2. Run dry-run scan.
3. Review `_System/SCAN_REPORT.md` and `_System/PRIVACY_REVIEW.md`.
4. Confirm import plan.
5. Execute import only after approval.
6. Review logs and manual review queue.

## Dry-run

```bash
cd /Users/ditang/obsidian/obsidian-vault-builder
python scripts/scan_sources.py --config config/sources.yaml --dry-run
```

## Safe Full Regeneration

```bash
cd /Users/ditang/obsidian/obsidian-vault-builder
python scripts/generate_all.py --config config/sources.yaml
```

This rebuilds scaffold checks, reports, indexes, context packs, DocMind execution pages, GTM operating pages, and `_System/COMPLETION_AUDIT.md` from the current inventory. It does not refresh the URL scan unless `--refresh-scan` is provided, and it does not execute imports unless `--execute-import --confirmed` is provided.

## Rollback

Rollback must only delete files generated by this system in a recorded import batch. Originals are never touched.

```bash
cd /Users/ditang/obsidian/obsidian-vault-builder
python scripts/rollback_import.py --last
```

## Manual Review

Manual review is tracked in `_System/MANUAL_REVIEW.md`. Current private/local sources are disabled; browser cookies, sessions, password stores, Keychain, email, chats, and broad local folders are outside scope until a separate source plan is approved.
"""

IMPORT_PLAN = """# IMPORT_PLAN

## Status

Gate A has a safe starter source selected: `URL List`.

- Enabled source: `URL List`
- Path: `obsidian-vault-builder/data/urls.txt`
- Network: disabled
- Read file contents: disabled
- Latest dry-run records: 0, because the URL list currently has no real URL lines

## Recommended First Dry-run

- Browser Bookmarks Export: low risk if it is a manually exported HTML file.
- Readwise Export: medium risk, exported reading notes only.
- Notion Export: medium risk, review folder contents before enabling.
- URL List: low risk when `allow_network: false`; generates URL source notes only.

## Higher-risk Sources

- Desktop, Documents, Downloads: broad personal folders, enable only one at a time.
- iCloud Drive, Google Drive, Dropbox, OneDrive: high privacy risk, enable only after narrowing to an export subfolder.
- GitHub Local Repos: medium risk; should only summarize README/docs and skip secrets.

## Not Recommended For First Scan

- Whole home directory.
- Whole cloud drives.
- Email exports.
- Chat exports.
- Browser cookie/session/password stores.
- Bank, tax, medical, passport, legal, customer-sensitive, or credential folders.

## Required Confirmation

To produce inventory records, add one URL per line to `data/urls.txt` or enable exactly one low-risk export source in `config/sources.yaml`, then run dry-run again.
"""

SOURCES_DOC = """# SOURCES

Source configuration lives in:

`/Users/ditang/obsidian/obsidian-vault-builder/config/sources.yaml`

Current enabled source:

- `URL List`: `./data/urls.txt`

All broad personal folders remain disabled:

- Desktop
- Documents
- Downloads
- iCloud Drive
- Google Drive
- Dropbox
- OneDrive
- GitHub local repos
"""

RULES_DOC = """# RULES

Rules live in:

- `config/rules.yaml`
- `config/privacy_rules.yaml`
- `config/classification_rules.yaml`

The default posture is dry-run, metadata-first, no content reading, no network, no OCR, no transcription, and no online AI.
"""
