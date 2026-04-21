# Obsidian Investment System

## Scope

This vault is used for investment research, project tracking, reporting, and system operations.

Agents working in this vault must preserve structure, avoid duplication, and keep notes easy to navigate.

## Core Structure

- `00_Dashboard` -> dashboards, indexes, and entry points
- `01_Wiki` -> evergreen knowledge, frameworks, models, and reference notes
- `02_Research` -> new opportunities under evaluation
- `03_Projects` -> active approved projects
- `04_Reports` -> formal outputs and reporting
- `09_System` -> agents, skills, rules, templates, workflows, and shared resources

## Folder Rules

- Do not modify `.obsidian/` unless explicitly instructed.
- Follow the folder structure strictly.
- Do not create new top-level folders unless explicitly instructed.
- Keep project names in Chinese unless a project already has an established English name.
- Prefer using existing folders before creating new parallel structures.

## Research Folder Rules

Research notes must be organized by domain first, then by status.

Supported domains:

- `02_Research/AI研究`
- `02_Research/政策研究`
- `02_Research/项目研究`

`AI研究` and `政策研究` should contain:

- `研究中`
- `结论`
- `参考资料`

`项目研究` should contain:

- `在研究`
- `推进中`
- `不买`

Templates are stored centrally in:

- `99_System/Templates/Research`
- `99_System/Templates/Projects`
- `99_System/Templates/Reports`

When creating a new research note, choose the closest matching domain first.

For `AI研究` and `政策研究`, default to `研究中`.

For `项目研究`, default to `在研究` unless the user explicitly asks for a different status.

## Project Folder Rules

Approved opportunities should move into `03_Projects`.

Use `99_System/Templates/Projects` as the source for reusable project structure.

Each active project should have its own folder under `03_Projects`, for example `10_Projects/灰石项目`.

## Report Folder Rules

Reports must be stored in one of these folders:

- `30_Reports/投资评估报告`
- `30_Reports/项目报告`
- `99_System/Templates/Reports`

Use the matching template in `99_System/Templates/Reports` before creating a new report when a template exists.

## Naming Rules

- Use concise, descriptive file names.
- Avoid duplicate notes with slightly different names.
- Keep folder names stable once links already depend on them.
- Use Chinese naming for project folders and project-facing documents by default.
- Use `DD-MM-YYYY` for dates when dates appear in titles, metadata, or body text.

## Required Research Note Structure

Each research note should contain at least:

- Basic Info
- Thesis
- Risks
- Next Steps

Recommended metadata fields:

- `status`
- `created`
- `updated`
- `owner`
- `tags`

## Required Project Structure

Each project should include notes or sections covering:

- Overview
- Thesis
- Updates
- Actions
- Materials
- Meetings
- Decisions

Recommended metadata fields:

- `status`
- `project`
- `created`
- `updated`
- `owner`
- `tags`

## Workflow

When a new investment idea appears:

1. For `AI研究` and `政策研究`, create or update a note under `02_Research/<领域>/研究中`.
2. When the analysis is mature, move or summarize it into `02_Research/<领域>/结论`.
3. Store supporting source material under `02_Research/<领域>/参考资料` when needed.
4. For `项目研究`, create or update a note under `20_Knowledge/在研究`.
5. If project diligence deepens, move the note to `20_Knowledge/推进中`.
6. If rejected, move the note to `20_Knowledge/不买` and record the rejection reason.
7. If approved, create or move the working set into `10_Projects/<项目名>`.

## Linking Rules

- Prefer editing an existing note over creating a duplicate.
- Maintain links between related research, project, and report notes.
- Link reports back to the source research or project when relevant.
- Preserve existing backlinks when moving or renaming notes.

## Agent Behavior Rules

- Search for an existing relevant note before creating a new one.
- Prefer structured notes over free-form text.
- Prefer templates when available.
- Do not rename or move files unless the workflow requires it or the user requests it.
- Do not delete notes unless explicitly instructed.
- Keep changes minimal, clear, and consistent with the vault structure.

## Preferred Outputs

- Short structured notes over long unstructured prose
- Consistent headings across similar note types
- Reusable templates for repeated workflows
