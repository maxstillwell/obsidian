from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class URLMetadata:
    fetched: bool
    status_code: str
    content_type: str
    title: str
    error: str


def fetch_url_metadata(url: str, allow_network: bool, timeout: int = 10, max_bytes: int = 262144) -> URLMetadata:
    if not allow_network:
        return URLMetadata(False, "", "", "", "Network disabled; URL was not fetched.")
    request = Request(
        url,
        headers={
            "User-Agent": "FounderOS-Obsidian-Vault-Builder/0.1 (+metadata-only; no cookies)",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:  # nosec - public URL metadata fetch only
            body = response.read(max_bytes)
            content_type = response.headers.get("content-type", "")
            return URLMetadata(True, str(response.status), content_type, parse_html_title(body), "")
    except HTTPError as exc:
        body = exc.read(max_bytes)
        return URLMetadata(True, str(exc.code), exc.headers.get("content-type", ""), parse_html_title(body), str(exc))
    except URLError as exc:
        return URLMetadata(False, "", "", "", str(exc.reason))
    except OSError as exc:
        return URLMetadata(False, "", "", "", str(exc))


def parse_html_title(html: bytes) -> str:
    parser = _TitleParser()
    try:
        parser.feed(html.decode("utf-8", errors="replace"))
    except Exception:
        return ""
    return parser.title.strip()


class _TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self._parts: list[str] = []

    @property
    def title(self) -> str:
        return " ".join(part.strip() for part in self._parts if part.strip())

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._parts.append(data)
