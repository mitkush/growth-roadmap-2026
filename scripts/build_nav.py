"""Add navigation bars to every page of the course.

Run from the repository root: python3 scripts/build_nav.py
Safe to re-run: each bar sits between <!-- nav:top --> / <!-- nav:bottom --> markers and is replaced.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = sorted((ROOT / "steps").glob("0*.md"))
LESSON_DIRS = sorted((ROOT / "lessons").iterdir())
TOP = "<!-- nav:top -->"
BOTTOM = "<!-- nav:bottom -->"
END = "<!-- nav:end -->"


def title(path: Path) -> str:
    return re.search(r"^# (.+)$", path.read_text(), re.M).group(1).strip()


def step_name(path: Path) -> str:
    """'Step 1: Advanced Ruby: Concurrency, YJIT & Profiling' -> 'Advanced Ruby: Concurrency, YJIT & Profiling'."""
    return re.sub(r"^Step \d+: ", "", title(path))


def rel(target: Path, source: Path) -> str:
    return Path(os.path.relpath(target, source.parent)).as_posix()


def link(text: str, target: Path, source: Path, anchor: str = "") -> str:
    return f"[{text}]({rel(target, source)}{anchor})"


def set_nav(path: Path, top: str | None, bottom: str | None) -> None:
    """Replace only the nav regions; the rest of the file is left byte-for-byte unchanged."""
    text = path.read_text()
    text = re.sub(rf"\n{re.escape(TOP)}\n.*?\n{re.escape(END)}\n", "", text, flags=re.S)  # old top bar
    text = re.sub(rf"\n{re.escape(BOTTOM)}\n.*?\n{re.escape(END)}\n$", "", text, flags=re.S)  # old bottom bar
    if top:
        first, _, rest = text.partition("\n")  # the "# Title" line
        text = f"{first}\n\n{TOP}\n{top}\n{END}\n{rest}"
    if bottom:
        text = text.rstrip("\n") + f"\n\n{BOTTOM}\n\n---\n\n{bottom}\n{END}\n"
    path.write_text(text)


README, GLOSSARY = ROOT / "README.md", ROOT / "GLOSSARY.md"

# --- step plans ---------------------------------------------------------------
for i, step in enumerate(STEPS):
    n = i + 1
    start = LESSON_DIRS[i] / "00-start-here.md"
    top = " · ".join([link("Course home", README, step), f"Step {n} of {len(STEPS)}",
                      link(f"Step {n} lessons", start, step), link("Glossary", GLOSSARY, step)])
    prev = (link(f"← Step {n - 1}: {step_name(STEPS[i - 1])}", STEPS[i - 1], step) if i > 0
            else link("← How to use this roadmap", README, step, "#how-to-use-this-roadmap"))
    nxt = (link(f"Step {n + 1}: {step_name(STEPS[i + 1])} →", STEPS[i + 1], step) if i + 1 < len(STEPS)
           else link("Progress tracker →", README, step, "#progress-tracker"))
    bottom = f"{prev} · {link(f'Step {n} lessons', start, step)} · {nxt}"
    set_nav(step, top, bottom)

# --- lessons ------------------------------------------------------------------
for i, folder in enumerate(LESSON_DIRS):
    n = i + 1
    plan = STEPS[i]
    pages = sorted(folder.glob("[0-9][0-9]-*.md"))
    start = folder / "00-start-here.md"
    for j, page in enumerate(pages):
        crumbs = [link("Course home", README, page), link(f"Step {n} plan", plan, page)]
        if page != start:
            crumbs.append(link(f"Step {n} lessons", start, page))
        crumbs.append(link("Glossary", GLOSSARY, page))
        top = " › ".join(crumbs[:-1]) + " · " + crumbs[-1]
        if page == start:
            prev = (link(f"← Step {n - 1} lessons", LESSON_DIRS[i - 1] / "00-start-here.md", page) if i > 0
                    else link("← Course home", README, page))
            first = link(f"First lesson: {title(pages[1])} →", pages[1], page) if len(pages) > 1 else ""
            nxt = (link(f"Step {n + 1} lessons →", LESSON_DIRS[i + 1] / "00-start-here.md", page)
                   if i + 1 < len(LESSON_DIRS) else "")
            bottom = " · ".join(x for x in [prev, link(f"Step {n} plan", plan, page), first, nxt] if x)
        else:
            prev = link(f"← {title(pages[j - 1])}", pages[j - 1], page)
            if j + 1 < len(pages):
                nxt = link(f"{title(pages[j + 1])} →", pages[j + 1], page)
            else:
                nxt = link(f"Back to the Step {n} plan →", plan, page)
            bottom = f"{prev} · {link(f'Step {n} lessons', start, page)} · {nxt}"
        set_nav(page, top, bottom)

# --- starters, templates, changes, glossary ------------------------------------
home_only = [ROOT / "CHANGES.md", *sorted((ROOT / "templates").glob("*.md"))]
for page in home_only:
    set_nav(page, f"{link('Course home', README, page)} · {link('Glossary', GLOSSARY, page)}",
            f"{link('← Course home', README, page)}")

for page, steps in [(ROOT / "starters/shop-lab/README.md", [1, 2, 3]), (ROOT / "starters/kb-api/README.md", [6, 7])]:
    used = " · ".join(link(f"Step {s} plan", STEPS[s - 1], page) for s in steps)
    note = " (course links: they stop working after you copy this folder into your own repository)" if "kb-api" in str(page) else ""
    set_nav(page, f"{link('Course home', README, page)} · Used in: {used}{note}", f"{link('← Course home', README, page)} · {used}")

set_nav(GLOSSARY, f"{link('Course home', GLOSSARY.with_name('README.md'), GLOSSARY)} · Steps: "
        + " · ".join(link(str(k + 1), s, GLOSSARY) for k, s in enumerate(STEPS)), None)

# --- README: quick jump line ------------------------------------------------------
set_nav(README, "**Jump to:** [How to use this roadmap](#how-to-use-this-roadmap) · [Steps](#steps) · "
        "[Calendar](#week-by-week-calendar) · [Progress tracker](#progress-tracker) · "
        f"[Start Step 1]({rel(STEPS[0], README)}) · [Glossary](GLOSSARY.md)", None)
print("navigation written")
