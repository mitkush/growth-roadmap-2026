"""Build GLOSSARY.md from the glossary tables in lessons/*/00-start-here.md.

Run from the repository root: python3 scripts/build_glossary.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEP_NAMES = {
    "01": "Advanced Ruby", "02": "Rails at scale", "03": "Architecture", "04": "Open source",
    "05": "Python fundamentals", "06": "Applied Python", "07": "Agentic AI", "08": "AI tool MVP",
}
ROW = re.compile(r"^\| (\*\*.+?\*\*.*?) \| (.+) \| (.+) \|\s*$")
LINK = re.compile(r"\]\(([^)]+)\)")


def rows(start_here: Path):
    in_glossary = False
    for line in start_here.read_text().splitlines():
        if line.startswith("## "):
            in_glossary = "glossary" in line.lower()
            continue
        if in_glossary and (m := ROW.match(line)):
            yield m.groups()


entries = []
for folder in sorted((ROOT / "lessons").iterdir()):
    step = folder.name[:2]
    for term, meaning, lessons in rows(folder / "00-start-here.md"):
        lessons = LINK.sub(lambda m: f"](lessons/{folder.name}/{m.group(1)})", lessons)
        key = re.sub(r"^[^a-z0-9]+", "", re.sub(r"[*`_]", "", term).lower())
        entries.append((key, term, meaning, f"{step} {STEP_NAMES[step]}", lessons))

entries.sort(key=lambda e: (e[0], e[3]))
out = [
    "# Glossary",
    "",
    "Every term defined in the course, A to Z, with the step and the lesson that explains it.",
    "Generated from the glossary in each `lessons/*/00-start-here.md` by `python3 scripts/build_glossary.py`;",
    "edit those files, not this one. Some terms appear twice because two steps use them in different contexts.",
    "",
]
letter = None
for key, term, meaning, step, lessons in entries:
    first = key[0].upper() if key[0].isalpha() else "#"
    if first != letter:
        letter = first
        out += ["", f"## {letter}", "", "| Term | Meaning | Step | Lesson |", "|---|---|---|---|"]
    out.append(f"| {term} | {meaning} | {step} | {lessons} |")
(ROOT / "GLOSSARY.md").write_text("\n".join(out) + "\n")
print(f"{len(entries)} terms written to GLOSSARY.md")
