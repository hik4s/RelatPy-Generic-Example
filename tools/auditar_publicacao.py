from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env($|\.)", re.I),
    re.compile(r"(^|/)(downloads|logs|status|screenshots|artifacts|evidence)(/|$)", re.I),
    re.compile(r"(^|/)(relatorios|reports)(/|$)", re.I),
    re.compile(r"\.(csv|xlsx?|sqlite3?|db|har|trace|webm)$", re.I),
)

SUSPICIOUS_CONTENT_PATTERNS = {
    "URL privada ou endereço local": re.compile(
        r"https?://(?!(?:127\.0\.0\.1|localhost|example\.com))(?:[^\s\"'<>]+)",
        re.I,
    ),
    "Caminho UNC": re.compile(r"\\\\[A-Za-z0-9_.-]+\\[^\s\"']+"),
    "Possível segredo": re.compile(
        r"(?i)(password|passwd|senha|token|secret|api[_-]?key)\s*[:=]\s*[\"']?[^\s\"']{4,}"
    ),
    "E-mail": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
}

TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".json", ".toml", ".yaml", ".yml",
    ".ini", ".cfg", ".ps1", ".bat", ".gitignore", ".example",
}

ALLOWED_PUBLIC_URLS = {
    "https://example.com/REDACTED",
}


def tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [path for path in ROOT.rglob("*") if path.is_file()]

    return [
        ROOT / item.decode("utf-8", errors="replace")
        for item in result.stdout.split(b"\0")
        if item
    ]


def is_text_file(path: Path) -> bool:
    return path.name == ".gitignore" or path.suffix.lower() in TEXT_SUFFIXES


def main() -> int:
    findings: list[str] = []

    for path in tracked_files():
        try:
            relative = path.relative_to(ROOT).as_posix()
        except ValueError:
            continue

        for pattern in FORBIDDEN_PATH_PATTERNS:
            if pattern.search(relative):
                findings.append(f"[ARQUIVO PROIBIDO] {relative}")
                break

        if not path.is_file() or not is_text_file(path):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        for description, pattern in SUSPICIOUS_CONTENT_PATTERNS.items():
            for match in pattern.finditer(content):
                value = match.group(0)
                if value in ALLOWED_PUBLIC_URLS:
                    continue
                line = content.count("\n", 0, match.start()) + 1
                findings.append(
                    f"[CONTEÚDO SUSPEITO] {relative}:{line} - {description}"
                )

    if findings:
        print("Publicação bloqueada. Revise os itens abaixo:\n")
        for finding in sorted(set(findings)):
            print(f"- {finding}")
        return 1

    print("Auditoria concluída: nenhum indicador sensível conhecido foi encontrado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
