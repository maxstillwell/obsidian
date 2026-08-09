from dataclasses import dataclass


PROJECT_KEYWORDS = {
    "DocMind": [
        "docmind",
        "customer support",
        "ai support",
        "shopify",
        "gorgias",
        "customer service",
        "helpdesk",
        "support automation",
        "customer pain",
        "sales objection",
        "seo strategy",
        "growth experiment",
        "icp",
        "roadmap",
    ],
    "221B": [
        "221b",
        "ai search",
        "verification",
        "citation",
        "citations",
        "web search",
        "source attribution",
        "source verification",
        "attribution",
        "faithfulness",
        "rag",
        "retrieval augmented generation",
        "arxiv",
        "research workflow",
        "answer engine",
        "search agent",
    ],
}

AREA_KEYWORDS = {
    "AI Workflows": ["prompt", "agent", "codex", "claude", "claude code", "chatgpt", "workflow", "automation", "skill", "eval", "tools", "best-practices", "responses", "function calling", "file search", "migration", "migrate"],
    "Content": ["seo", "blog", "content", "article", "keyword", "brief", "draft", "linkedin", "twitter", "x thread"],
    "Research": ["paper", "research", "rag", "retrieval", "retrieval augmented generation", "llm", "benchmark", "citation", "attribution", "faithfulness", "verification", "arxiv", "obsidian", "bases", "properties", "pkm", "knowledge management"],
    "Meetings": ["meeting", "call", "transcript", "notes", "customer interview", "follow up"],
    "Decision": ["decision", "decided", "tradeoff", "options", "choose", "rationale"],
}


@dataclass(frozen=True)
class ClassificationResult:
    project: str
    area: str
    confidence: str
    reason: str


def _score(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def classify_metadata(*parts: str) -> ClassificationResult:
    text = " ".join(str(part) for part in parts if part).lower()
    project_scores = {project: _score(text, keywords) for project, keywords in PROJECT_KEYWORDS.items()}
    area_scores = {area: _score(text, keywords) for area, keywords in AREA_KEYWORDS.items()}

    project, project_score = max(project_scores.items(), key=lambda item: item[1])
    area, area_score = max(area_scores.items(), key=lambda item: item[1])

    project_value = project if project_score else ""
    area_value = area if area_score else "Resource"
    best_score = max(project_score, area_score)
    confidence = "high" if best_score >= 3 else "medium" if best_score >= 1 else "low"
    reasons = []
    if project_score:
        reasons.append(f"project={project}:{project_score}")
    if area_score:
        reasons.append(f"area={area}:{area_score}")
    return ClassificationResult(
        project=project_value,
        area=area_value,
        confidence=confidence,
        reason=", ".join(reasons) or "No classification keywords matched",
    )
