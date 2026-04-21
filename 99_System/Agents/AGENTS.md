# Obsidian Investment System

## Scope

This vault is used for investment research, project tracking, reporting, and system operations.

Agents working in this vault must preserve structure, avoid duplication, and keep notes easy to navigate.

## Core Structure

- `00_Dashboard` -> dashboards, indexes, and entry points
- `00_Inbox` -> raw source intake and temporary holding area
- `10_Projects` -> active project workspaces
- `20_Knowledge` -> flat evergreen knowledge and tagged research notes
- `30_Reports` -> drafts, finals, and report examples
- `90_Archive` -> completed or abandoned work
- `99_System` -> agents, skills, rules, templates, workflows, and shared resources

## Folder Rules

- Do not modify `.obsidian/` unless explicitly instructed.
- Follow the folder structure strictly.
- Do not create new top-level folders unless explicitly instructed.
- Keep project names in Chinese unless a project already has an established English name.
- Prefer using existing folders and index notes before creating new parallel structures.
- Use tags to classify notes; use folders to separate workflow stages.

## Knowledge Rules

`20_Knowledge` is intentionally flat.

Use tags and links instead of nested topic folders.

Keep only concrete knowledge notes here; do not create extra MOC pages unless they are truly needed for navigation.

## Project Rules

Approved opportunities should move into `10_Projects/<项目名>`.

Each active project should have an index note plus working notes such as:

- `index.md`
- `项目总览.md` or equivalent overview note
- `资料清单.md` or source log
- `analysis.md` or analysis note
- `decision-log.md` or decision note
- `report-draft.md` or draft output

Use `99_System/Templates/Projects` as the source for reusable project structure.

## Report Rules

Reports must be stored in one of these folders:

- `30_Reports/drafts`
- `30_Reports/finals`
- `30_Reports/examples`

Use the matching template in `99_System/Templates/Reports` before creating a new report when a template exists.

## Naming Rules

- Use concise, descriptive file names.
- Avoid duplicate notes with slightly different names.
- Keep folder names stable once links already depend on them.
- Use Chinese naming for project folders and project-facing documents by default.
- Use `DD-MM-YYYY` for dates when dates appear in titles, metadata, or body text.

## Required Note Structure

Prefer notes to include at least one of the following sections when relevant:

- Overview
- Thesis
- Risks
- Next Steps
- Related Links

Recommended metadata fields:

- `status`
- `created`
- `updated`
- `owner`
- `tags`
- `project`
- `report_type`

## Workflow

When a new investment idea appears:

1. Store raw material in `00_Inbox`.
2. For project research, create or update the relevant project workspace under `10_Projects/<项目名>`.
3. If a project analysis matures into a stable conclusion, summarize the result into `20_Knowledge`.
4. If approved, keep working material in the project workspace and emit reports into `30_Reports`.
5. If rejected or finished, move the working set into `90_Archive`.

## Linking Rules

- Prefer editing an existing note over creating a duplicate.
- Maintain links between related research, project, and report notes.
- Link reports back to the source research or project when relevant.
- Preserve existing backlinks when moving or renaming notes.
- Build hub/index notes for each major project or knowledge family only when they add clear value.

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
