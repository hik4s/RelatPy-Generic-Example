from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSOR = "#&$&@&$&#@&"

TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".json", ".toml", ".yaml", ".yml",
    ".ini", ".cfg", ".ps1", ".bat", ".gitignore", ".example",
    ".css", ".js", ".ts", ".tsx", ".jsx",
}

# Arquivos/pastas que não devem existir em uma publicação pública.
FORBIDDEN_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env($|\.)", re.I),
    re.compile(r"(^|/)(downloads|logs|status|screenshots|artifacts|evidence)(/|$)", re.I),
    re.compile(r"(^|/)(relatorios|reports)(/|$)", re.I),
    re.compile(r"(^|/)(auth[_-]?state|cookies|secrets|credentials)(/|$)", re.I),
    re.compile(r"\.(csv|xlsx?|ods|parquet|sqlite3?|db|har|trace|webm)$", re.I),
)

# Conteúdo que será substituído apenas no trecho correspondente.
CONTENT_RULES = (
    (
        "url_externa_ou_privada",
        re.compile(
            r"https?://(?!(?:127\.0\.0\.1|localhost|example\.com)(?:[:/]|$))"
            r"[^\s\"'<>`]+",
            re.I,
        ),
        "https://example.com/REDACTED",
    ),
    (
        "caminho_unc",
        re.compile(r"\\\\[A-Za-z0-9_.-]+\\[^\s\"'`]+"),
        r"\SERVIDOR_EXEMPLO\CAMINHO_CENSURADO",
    ),
    (
        "email",
        re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
        "usuario@example.com",
    ),
    (
        "ipv4_privado",
        re.compile(
            r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|"
            r"192\.168\.\d{1,3}\.\d{1,3})(?![\d.])"
        ),
        "192.0.2.1",
    ),
    (
        "possivel_segredo_atribuido",
        re.compile(
            r"(?i)(?P<key>password|passwd|senha|token|secret|api[_-]?key)"
            r"(?P<sep>\s*[:=]\s*)"
            r"(?P<quote>[\"']?)"
            r"(?P<value>[^\s,;\"']{4,})"
            r"(?P=quote)"
        ),
        None,
    ),
)

# Termos obrigatoriamente censurados na versão pública.
# As palavras são montadas em partes para o sanitizador não detectar
# o próprio código-fonte como ocorrência sensível.
BUILTIN_FORBIDDEN_TERMS = (
    "sg" + "ind",
    "i" + "qos",
)

# Termos específicos adicionais podem ser configurados localmente sem versionar.
TERMS_FILE = ROOT / "publication_terms.local.txt"


@dataclass
class Finding:
    action: str
    path: str
    rule: str
    line: int | None = None
    occurrences: int = 1


def git_tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]

    return [
        ROOT / value.decode("utf-8", errors="replace")
        for value in result.stdout.split(b"\0")
        if value
    ]


def forbidden_path(relative: str) -> str | None:
    for pattern in FORBIDDEN_PATH_PATTERNS:
        if pattern.search(relative):
            return pattern.pattern
    return None


def is_text(path: Path) -> bool:
    return path.name == ".gitignore" or path.suffix.lower() in TEXT_SUFFIXES


def load_custom_terms() -> list[str]:
    terms = list(BUILTIN_FORBIDDEN_TERMS)

    if not TERMS_FILE.is_file():
        return terms

    for line in TERMS_FILE.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            terms.append(value)

    # Remove repetições sem perder a ordem e sem diferenciar maiúsculas.
    unique_terms: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized = term.casefold()
        if normalized not in seen:
            seen.add(normalized)
            unique_terms.append(term)

    return unique_terms


def redact_secret(match: re.Match[str]) -> str:
    return (
        match.group("key")
        + match.group("sep")
        + '"'
        + CENSOR
        + '"'
    )


def sanitize_content(content: str, custom_terms: list[str]) -> tuple[str, list[tuple[str, int, int]]]:
    updated = content
    changes: list[tuple[str, int, int]] = []

    for rule, pattern, replacement in CONTENT_RULES:
        matches = list(pattern.finditer(updated))
        if not matches:
            continue

        lines = sorted({updated.count("\n", 0, m.start()) + 1 for m in matches})
        if rule == "possivel_segredo_atribuido":
            updated = pattern.sub(redact_secret, updated)
        else:
            updated = pattern.sub(replacement, updated)

        for line in lines:
            changes.append((rule, line, len(matches)))

    for term in custom_terms:
        pattern = re.compile(re.escape(term), re.I)
        matches = list(pattern.finditer(updated))
        if not matches:
            continue
        lines = sorted({updated.count("\n", 0, m.start()) + 1 for m in matches})
        updated = pattern.sub(CENSOR, updated)
        for line in lines:
            changes.append(("termo_personalizado", line, len(matches)))

    return updated, changes


def unique_quarantine_target(base: Path, relative: Path) -> Path:
    target = base / relative
    if not target.exists():
        return target
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return target.with_name(f"{target.name}.{timestamp}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Sanitiza uma cópia pública do repositório. Por padrão, apenas simula."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica censura e move arquivos proibidos para quarentena.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma automaticamente o modo --apply.",
    )
    parser.add_argument(
        "--include-untracked",
        action="store_true",
        help="Também examina arquivos não rastreados dentro do projeto.",
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = ROOT.parent / f"{ROOT.name}_backup_publicacao_{timestamp}"
    quarantine_root = ROOT.parent / f"{ROOT.name}_quarentena_{timestamp}"
    report_path = ROOT / f"sanitization_report_{timestamp}.json"

    files = git_tracked_files()
    if args.include_untracked:
        existing = {p.resolve() for p in files if p.exists()}
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts and path.resolve() not in existing:
                files.append(path)

    custom_terms = load_custom_terms()
    findings: list[Finding] = []
    planned_text_changes: list[tuple[Path, str, list[tuple[str, int, int]]]] = []
    planned_quarantine: list[tuple[Path, Path, str]] = []

    for path in files:
        if not path.exists() or not path.is_file():
            continue
        try:
            relative_path = path.relative_to(ROOT)
        except ValueError:
            continue
        relative = relative_path.as_posix()

        rule = forbidden_path(relative)
        if rule:
            target = unique_quarantine_target(quarantine_root, relative_path)
            planned_quarantine.append((path, target, rule))
            findings.append(Finding("quarantine", relative, rule))
            continue

        if not is_text(path):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        sanitized, changes = sanitize_content(content, custom_terms)
        if sanitized != content:
            planned_text_changes.append((path, sanitized, changes))
            for rule_name, line, occurrences in changes:
                findings.append(
                    Finding("redact", relative, rule_name, line, occurrences)
                )

    print("\nResumo da sanitização")
    print("=" * 72)
    print(f"Modo: {'APLICAÇÃO' if args.apply else 'SIMULAÇÃO'}")
    print(f"Arquivos para quarentena: {len(planned_quarantine)}")
    print(f"Arquivos de texto para censura: {len(planned_text_changes)}")
    print(f"Detecções: {len(findings)}")

    for finding in findings:
        location = finding.path
        if finding.line:
            location += f":{finding.line}"
        print(f"- {finding.action.upper():10} {location} [{finding.rule}]")

    if not args.apply:
        print("\nNenhum arquivo foi alterado.")
        print("Execute novamente com --apply para aplicar as mudanças.")
        return 1 if findings else 0

    if findings and not args.yes:
        answer = input(
            "\nSerá criado backup antes das alterações. Digite SANITIZAR para continuar: "
        ).strip()
        if answer != "SANITIZAR":
            print("Operação cancelada. Nenhum arquivo foi alterado.")
            return 2

    if not findings:
        print("Nenhuma alteração necessária.")
        return 0

    backup_root.mkdir(parents=True, exist_ok=False)

    # Copia para backup somente o que será alterado ou movido.
    for path, _, _ in planned_quarantine:
        relative = path.relative_to(ROOT)
        backup = backup_root / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)

    for path, _, _ in planned_text_changes:
        relative = path.relative_to(ROOT)
        backup = backup_root / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)

    # Move arquivos proibidos para fora do repositório.
    for source, target, _ in planned_quarantine:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))

    # Censura somente os trechos detectados.
    for path, sanitized, _ in planned_text_changes:
        path.write_text(sanitized, encoding="utf-8")

    report = {
        "created_at": datetime.now().isoformat(),
        "root": str(ROOT),
        "backup": str(backup_root),
        "quarantine": str(quarantine_root),
        "findings": [asdict(f) for f in findings],
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\nSanitização aplicada.")
    print(f"Backup: {backup_root}")
    print(f"Quarentena: {quarantine_root}")
    print(f"Relatório: {report_path}")
    print("\nRevise git diff e execute novamente o auditor antes do commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
