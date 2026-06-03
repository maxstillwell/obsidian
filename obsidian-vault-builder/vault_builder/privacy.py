from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


CRITICAL_PATTERNS = {
    ".env",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    ".pem",
    ".key",
    "credentials.json",
    "token.json",
    "secret",
    "secrets",
    "private_key",
    "api_key",
    "apikey",
    "password",
    "passport",
    "identity",
    "medical",
    "bank",
    "tax",
    "legal",
}

HIGH_PATTERNS = {
    "email",
    "mailbox",
    "chat",
    "customer data",
    "contract",
    "invoice",
    "payroll",
    "personal",
}


@dataclass(frozen=True)
class PrivacyAssessment:
    level: str
    secret_risk: bool
    import_action: str
    needs_manual_review: bool
    reason: str


def assess_privacy(path_or_name: str, configured_level: str | None = None) -> PrivacyAssessment:
    path = Path(path_or_name)
    basename = path.name.lower()
    full = str(path_or_name).lower()

    for pattern in CRITICAL_PATTERNS:
        if basename == pattern or pattern in basename or pattern in full:
            return PrivacyAssessment(
                level="critical",
                secret_risk=True,
                import_action="skip",
                needs_manual_review=True,
                reason=f"Matched critical privacy pattern: {pattern}",
            )

    for pattern in HIGH_PATTERNS:
        if pattern in full:
            return PrivacyAssessment(
                level="high",
                secret_risk=False,
                import_action="index_only",
                needs_manual_review=True,
                reason=f"Matched high privacy pattern: {pattern}",
            )

    if configured_level in {"high", "critical"}:
        return PrivacyAssessment(
            level=configured_level,
            secret_risk=False,
            import_action="index_only" if configured_level == "high" else "skip",
            needs_manual_review=True,
            reason=f"Source configured as {configured_level} privacy",
        )

    return PrivacyAssessment(
        level=configured_level or "low",
        secret_risk=False,
        import_action="metadata_note",
        needs_manual_review=False,
        reason="No sensitive pattern matched",
    )
