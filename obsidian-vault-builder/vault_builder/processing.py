from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from .classification import classify_metadata


@dataclass(frozen=True)
class ExtractResult:
    text: str
    truncated: bool
    error: str


def classify_inventory_records(records: list[dict]) -> list[dict]:
    updated: list[dict] = []
    for record in records:
        copy = dict(record)
        result = classify_metadata(
            copy.get("filename", ""),
            copy.get("original_path", ""),
            copy.get("source_name", ""),
            copy.get("source_url", ""),
        )
        copy["suggested_project"] = result.project
        copy["suggested_area"] = result.area
        copy["classification_confidence"] = result.confidence
        copy["classification_reason"] = result.reason
        updated.append(copy)
    return updated


def extract_text_file(path: Path | str, max_chars: int = 12000) -> ExtractResult:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    try:
        if suffix in {".txt", ".md", ".csv"}:
            return _read_text(file_path, max_chars)
        if suffix in {".html", ".htm"}:
            raw = file_path.read_text(encoding="utf-8", errors="replace")
            parser = _TextHTMLParser()
            parser.feed(raw)
            return _truncate(parser.text(), max_chars)
        if suffix == ".pdf":
            return _extract_pdf(file_path, max_chars)
        if suffix == ".docx":
            return _extract_docx(file_path, max_chars)
    except OSError as exc:
        return ExtractResult("", False, str(exc))
    except Exception as exc:  # Dependency parsers should not crash the workflow.
        return ExtractResult("", False, f"Extraction failed: {exc}")
    return ExtractResult("", False, f"Unsupported extension for text extraction: {suffix or 'none'}")


def _read_text(path: Path, max_chars: int) -> ExtractResult:
    return _truncate(path.read_text(encoding="utf-8", errors="replace"), max_chars)


def _truncate(text: str, max_chars: int) -> ExtractResult:
    if len(text) <= max_chars:
        return ExtractResult(text, False, "")
    return ExtractResult(text[:max_chars], True, "")


def _extract_pdf(path: Path, max_chars: int) -> ExtractResult:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ExtractResult("", False, "pypdf is not installed; PDF extraction skipped.")
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
        joined = "\n".join(parts)
        if len(joined) >= max_chars:
            return _truncate(joined, max_chars)
    return _truncate("\n".join(parts), max_chars)


def _extract_docx(path: Path, max_chars: int) -> ExtractResult:
    try:
        import docx
    except ImportError:
        return ExtractResult("", False, "python-docx is not installed; DOCX extraction skipped.")
    document = docx.Document(str(path))
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    return _truncate(text, max_chars)


class _TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self._parts.append(stripped)

    def text(self) -> str:
        return "\n".join(self._parts)
