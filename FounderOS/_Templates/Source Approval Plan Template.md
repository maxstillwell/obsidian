# Source Approval Plan Template

<!-- founderos-daily-operating:start -->
---
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
<!-- founderos-daily-operating:end -->
