#!/usr/bin/env python3
"""Normalize book/*.md from pdftotext-layout dumps into consistent Markdown."""

from __future__ import annotations

import re
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1] / "book"
PDF = "https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf"
SOURCE = "Richards J. Heuer, Jr., *Psychology of Intelligence Analysis* (CSI/CIA, 1999)."

SKIP = {"00-index.md", "_source-cleaned.md"}

PAGE_NUM = re.compile(r"^\d{1,3}$")
ROMAN = re.compile(r"^(?:[ivxlcdm]{1,8})$", re.I)
ORNAMENT = re.compile(r"^\*{3,}$")
FOOTNOTE_START = re.compile(r"^(\d{1,3})\.\s+(.*)$")
CHAPTER_LINE = re.compile(r"^Chapter\s+(\d+)\b(.*)$", re.I)
STEP_LINE = re.compile(r"^Step\s+(\d+)\s*$", re.I)
PART_LINE = re.compile(r"^PART\s+[IVX]+\b(.*)$", re.I)
ALREADY_HEADING = re.compile(r"^#{1,6}\s+")
LIST_ITEM = re.compile(r"^(\d+)\.\s+\S")
BULLET = re.compile(r"^[•\-]\s+")
# ACH step-by-step outline (must stay in body, not ## Footnotes)
ACH_OUTLINE = re.compile(
    r"^(?:Identify the possible hypotheses|Make a list of significant evidence|"
    r"Prepare a matrix with hypotheses|Refine the matrix\.|"
    r"Draw tentative conclusions about the relative|"
    r"Analyze how sensitive your conclusion|"
    r"Report conclusions\.|"
    r"Identify milestones for future observation)",
    re.I,
)
BIBLIO_HINT = re.compile(
    r"(?:"
    r"\b(?:Press|University|ibid|Studies in Intelligence|Technical Report)\b|"
    r"\bVol\.\s|\bpp\.\s|\b(?:ed|eds)\.\s|op\.\s*cit|"
    r"\(\d{4}\)|\d{4}\)|"  # (1991) or ..., 1991)
    r"(?:^|\s)[A-Z][a-zA-Z'\-]+,\s+(?:The |A |An )?[\"'A-Z]"  # Wirtz, The ...
    r")"
)

OCR_FIXES = [
    (re.compile(r"\bfashed\b"), "flashed"),
    (re.compile(r"\bbriefy\b"), "briefly"),
    (re.compile(r"\bmodifed\b"), "modified"),
    (re.compile(r"\bpaper fow\b"), "paper flow"),
    (re.compile(r"\blittle orno\b"), "little or no"),
    (re.compile(r"\bconfict(ing|s)?\b"), r"conflict\1"),
    (re.compile(r"\bspecifc(ally|ation|ations|ied)?\b"), r"specific\1"),
    (re.compile(r"\bspecifed\b"), "specified"),
    (re.compile(r"\bfourishes\b"), "flourishes"),
    (re.compile(r"\bTeoretical\b"), "Theoretical"),
    (re.compile(r"\bTeorem\b"), "Theorem"),
    (re.compile(r"\bOfensive\b"), "Offensive"),
    (re.compile(r"\bTeodore\b"), "Theodore"),
    (re.compile(r"\bStaf\b"), "Staff"),
    (re.compile(r"\bstaf\b"), "staff"),
    (re.compile(r"\bsufer(ing|ed|s)?\b"), r"suffer\1"),
    (re.compile(r"\bsuficient(ly)?\b"), r"sufficient\1"),
    (re.compile(r"\bsufice\b"), "suffice"),
    (re.compile(r"\bclarifes\b"), "clarifies"),
    (re.compile(r"\bofer\b"), "offer"),
    (re.compile(r"\bconceptuallydriven\b"), "conceptually-driven"),
    (re.compile(r"\blongterm\b"), "long-term"),
    (re.compile(r"everybody-thinkslike-us"), "everybody-thinks-like-us"),
    (re.compile(r"\bdiferent(ly|iate|iated|iation)?\b"), r"different\1"),
    (re.compile(r"\bdifering\b"), "differing"),
    (re.compile(r"\bdifcult(y|ies)?\b"), r"difficult\1"),
    (re.compile(r"\bimage\.(\d+)\s*"), ""),  # OCR: footnote marker glued to prior word
    (re.compile(r"\banalysis--"), "analysis—"),
    (re.compile(r"arguments- that"), "arguments—that"),
    (re.compile(r"numbers- for"), "numbers—for"),
    (re.compile(r"DDI- I\b"), "DDI-I"),
    (re.compile(r"\bviewand\s+ing\b"), "viewing"),
    (re.compile(r"\bstarted viewand\b"), "started viewing"),
    (re.compile(r"\bFischof\b"), "Fischhoff"),
]


def apply_ocr(text: str) -> str:
    for pat, repl in OCR_FIXES:
        text = pat.sub(repl, text)
    return text


def split_header_body(text: str) -> tuple[str, str, str, str]:
    """Return title, section_id, rest_of_header_unused, body."""
    lines = text.splitlines()
    title = "Untitled"
    section = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# ") and title == "Untitled":
            title = line[2:].strip()
        m = re.match(r"^Section:\s*(.+)\s*$", line)
        if m:
            section = m.group(1).strip()
        if line.strip().startswith("Do not load other book sections"):
            body_start = i + 1
            break
    body = "\n".join(lines[body_start:]).lstrip("\n")
    if not section:
        # derive from filename later
        section = "unknown"
    return title, section, "", body


def is_page_noise(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if ORNAMENT.match(s):
        return True
    if PAGE_NUM.match(s):
        return True
    # roman page markers like vii, xxv — exclude single "I" (could be list)
    if ROMAN.match(s) and len(s) >= 2:
        return True
    return False


def looks_bibliographic(text: str) -> bool:
    return bool(BIBLIO_HINT.search(text))


def is_footnote_item(num: int, first_text: str) -> bool:
    """True if 'N. text' is an endnote, not an ACH/body outline list item."""
    t = first_text.strip()
    if ACH_OUTLINE.match(t):
        return False
    if looks_bibliographic(t):
        return True
    # Low numbers that read like instructional outline stay in body
    if 1 <= num <= 8:
        return False
    return True


def footnote_complete(text: str) -> bool:
    """True if footnote text looks finished (terminal punctuation; ignore closing quotes)."""
    s = text.rstrip().rstrip("\"'")
    return s.endswith((".", "!", "?", ")"))


def footnote_continues(so_far: str, peek: str) -> bool:
    """After a blank line, should peek join the current footnote?"""
    p = peek.strip()
    if not p:
        return False
    if p.lower().startswith("op.") or p.lower().startswith("ibid"):
        return True
    done = footnote_complete(so_far)
    # Wrapped citation line: short, often lowercase continuation
    if p[:1].islower() and len(p) < 100 and not done:
        return True
    # Incomplete footnote (no terminal period yet) and lowercase wrap
    if p[:1].islower() and not done:
        return True
    return False


def extract_footnotes(lines: list[str]) -> tuple[list[str], dict[int, str]]:
    """Pull footnote blocks out; return remaining lines + footnotes dict."""
    footnotes: dict[int, str] = {}
    out: list[str] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        m = FOOTNOTE_START.match(s)
        if m and is_footnote_item(int(m.group(1)), m.group(2)):
            num = int(m.group(1))
            buf = [m.group(2)]
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt:
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j >= len(lines):
                        break
                    peek = lines[j].strip()
                    pm = FOOTNOTE_START.match(peek)
                    if pm and is_footnote_item(int(pm.group(1)), pm.group(2)):
                        break
                    if (
                        PAGE_NUM.match(peek)
                        or (ROMAN.match(peek) and len(peek) >= 2)
                        or ORNAMENT.match(peek)
                        or ALREADY_HEADING.match(peek)
                        or STEP_LINE.match(peek)
                        or peek.startswith("## ")
                    ):
                        break
                    # "Chapter N Title" heading vs prose "Chapter 4 discussed..."
                    cm = CHAPTER_LINE.match(peek)
                    if cm and _chapter_rest_is_title(cm.group(2)):
                        break
                    so_far = re.sub(r"\s+", " ", " ".join(buf)).strip()
                    # Multi-citation footnotes often continue after a page break
                    # with another Author, Title... line.
                    if looks_bibliographic(so_far) and looks_bibliographic(peek):
                        i = j
                        continue
                    # Body often resumes mid-sentence (lowercase) after a page
                    # break that interrupted the paragraph with a footnote.
                    # If the footnote already has a terminal period, stop.
                    if footnote_complete(so_far) and not footnote_continues(so_far, peek):
                        break
                    if footnote_continues(so_far, peek):
                        i = j
                        continue
                    break
                nm = FOOTNOTE_START.match(nxt)
                if nm and is_footnote_item(int(nm.group(1)), nm.group(2)):
                    break
                if STEP_LINE.match(nxt):
                    break
                cm = CHAPTER_LINE.match(nxt)
                if cm and _chapter_rest_is_title(cm.group(2)):
                    break
                if PAGE_NUM.match(nxt) or (ROMAN.match(nxt) and len(nxt) >= 2):
                    i += 1
                    continue
                if ORNAMENT.match(nxt):
                    i += 1
                    continue
                so_far = re.sub(r"\s+", " ", " ".join(buf)).strip()
                # New body paragraph after a complete footnote (no blank in dump)
                if (
                    footnote_complete(so_far)
                    and nxt[:1].isupper()
                    and len(nxt) > 50
                    and not looks_bibliographic(nxt)
                ):
                    break
                buf.append(nxt)
                i += 1
            text = apply_ocr(re.sub(r"\s+", " ", " ".join(buf)).strip())
            if num in footnotes:
                footnotes[num] = footnotes[num] + " " + text
            else:
                footnotes[num] = text
            continue
        out.append(raw)
        i += 1
    return out, footnotes


def _chapter_rest_is_title(rest: str) -> bool:
    """Reject prose like 'Chapter 4 discussed the weaknesses...'."""
    r = rest.strip(" :.-")
    if not r:
        return True  # bare "Chapter 8"
    if r[0].islower():
        return False
    # Long sentence-like tails are body prose, not titles
    if len(r.split()) > 14:
        return False
    if r.endswith("."):
        return False
    return True


def _part_rest_is_title(rest: str) -> bool:
    """Reject prose like 'Part I identifies some limitations...'."""
    r = rest.strip()
    if not r:
        return True
    if r[0] in "-–—:":
        return True
    if r[0].islower():
        return False
    if len(r.split()) > 12 or r.endswith("."):
        return False
    return True


def classify_heading(line: str) -> str | None:
    s = line.strip()
    if not s:
        return None
    if ALREADY_HEADING.match(s):
        # normalize ## Chapter wrappers from agent composites
        return s
    m = CHAPTER_LINE.match(s)
    if m and _chapter_rest_is_title(m.group(2)):
        rest = m.group(2).strip(" :.-")
        if rest:
            return f"## Chapter {m.group(1)}: {rest}"
        return f"## Chapter {m.group(1)}"
    if STEP_LINE.match(s):
        return f"## {s}"
    pm = PART_LINE.match(s)
    if pm and _part_rest_is_title(pm.group(1)):
        return f"## {s}"
    if s.lower().startswith("step-by-step outline"):
        return f"### {s}"
    # Known front-matter titles when alone on a line
    known = {
        "author's preface",
        "foreword",
        "introduction",
        "checklist for analysts",
        "summary and conclusion",
        "recommendations",
        "availability rule",
        "anchoring",
        "components of the memory system",
    }
    if s.lower() in known and len(s) < 80:
        return f"## {s}"
    return None


def looks_like_subtitle(line: str) -> bool:
    s = line.strip()
    if not s or len(s) > 100:
        return False
    if s.endswith("."):
        return False
    if classify_heading(s):
        return False
    # Title-ish: few words, often no lowercase start of long prose
    words = s.split()
    if 1 <= len(words) <= 14:
        return True
    return False


def reflow_body(lines: list[str]) -> list[str]:
    """Convert layout lines into markdown blocks (headings + paragraphs + lists)."""
    blocks: list[str] = []
    para: list[str] = []
    i = 0
    pending_chapter_num: str | None = None

    def flush_para() -> None:
        nonlocal para
        if not para:
            return
        text = apply_ocr(re.sub(r"\s+", " ", " ".join(para)).strip())
        if text:
            blocks.append(text)
        para = []

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s or is_page_noise(s):
            flush_para()
            i += 1
            continue

        # Drop duplicate chapter title lines right after ## Chapter N
        head = classify_heading(s)
        if head:
            flush_para()
            # If bare "## Chapter 8", absorb following subtitle line(s)
            m = re.match(r"^## Chapter (\d+)$", head)
            if m and i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if looks_like_subtitle(nxt) and not classify_heading(nxt):
                    head = f"## Chapter {m.group(1)}: {nxt}"
                    i += 1
            # Skip if this heading duplicates the last heading
            if blocks and blocks[-1] == head:
                i += 1
                continue
            # Also skip plain "Chapter 8" if we already have ## Chapter 8: Title
            blocks.append(head)
            i += 1
            continue

        # Numbered outline items (1. text) — footnotes already extracted
        if LIST_ITEM.match(s):
            flush_para()
            text = apply_ocr(re.sub(r"\s+", " ", s))
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or is_page_noise(nxt):
                    j = i
                    while j < len(lines) and (
                        not lines[j].strip() or is_page_noise(lines[j].strip())
                    ):
                        j += 1
                    if j >= len(lines):
                        break
                    peek = lines[j].strip()
                    if (
                        LIST_ITEM.match(peek)
                        or BULLET.match(peek)
                        or peek.startswith("•")
                        or classify_heading(peek)
                    ):
                        break
                    if not text.rstrip().endswith((".", "!", "?", ":", ";")) and (
                        peek[:1].islower() or len(peek.split()) < 12
                    ):
                        text = text + " " + apply_ocr(re.sub(r"\s+", " ", peek))
                        i = j + 1
                        continue
                    break
                if (
                    LIST_ITEM.match(nxt)
                    or BULLET.match(nxt)
                    or nxt.startswith("•")
                    or classify_heading(nxt)
                ):
                    break
                if not text.rstrip().endswith((".", "!", "?", ":", ";")):
                    text = text + " " + apply_ocr(re.sub(r"\s+", " ", nxt))
                    i += 1
                    continue
                if nxt[:1].islower():
                    text = text + " " + apply_ocr(re.sub(r"\s+", " ", nxt))
                    i += 1
                    continue
                break
            blocks.append(text)
            continue

        if BULLET.match(s) or s.startswith("•"):
            flush_para()
            text = apply_ocr(re.sub(r"\s+", " ", s))
            if text.startswith("•"):
                text = "- " + text[1:].strip()
            blocks.append(text)
            i += 1
            continue

        # Signature line
        if s.startswith("--") and "Heuer" in s:
            flush_para()
            blocks.append(f"*{s.lstrip('- ').strip()}*")
            i += 1
            continue

        para.append(s)
        i += 1

    flush_para()

    # Post-process: merge "Chapter N" heading with following title-only paragraph
    # already handled. Join list continuations that were split — skip for now.

    # Convert sequence of "1. ..." that are ACH outline into proper lists with blank lines
    out: list[str] = []
    for b in blocks:
        if out and out[-1].startswith("#") and b.startswith("#"):
            out.append("")
        elif out and out[-1].startswith("#"):
            out.append("")
        elif out and not out[-1].startswith("#") and b.startswith("#"):
            out.append("")
        out.append(b)
        # blank line after paragraphs (not after every list item crowding)
        if b.startswith("#"):
            continue
        if re.match(r"^\d+\.\s", b) or b.startswith("- "):
            continue
        out.append("")
    # trim trailing empties
    while out and out[-1] == "":
        out.pop()
    return out


def render(title: str, section: str, body_blocks: list[str], footnotes: dict[int, str]) -> str:
    parts = [
        f"# {title}",
        "",
        f"Source: {SOURCE}",
        f"PDF: {PDF}",
        f"Section: {section}",
        "",
        "Do not load other book sections unless the router names them.",
        "",
    ]
    parts.extend(body_blocks)
    if footnotes:
        parts.append("")
        parts.append("## Footnotes")
        parts.append("")
        for num in sorted(footnotes):
            parts.append(f"{num}. {footnotes[num]}")
            parts.append("")
    text = "\n".join(parts).rstrip() + "\n"
    # collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def normalize_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    title, section, _, body = split_header_body(raw)
    if section == "unknown":
        section = path.stem

    # Drop nested ## Chapter wrappers' duplicate content markers carefully
    body_lines = [ln.rstrip() for ln in body.splitlines()]

    # Remove page noise early
    cleaned = [ln for ln in body_lines if not (ln.strip() and is_page_noise(ln.strip()))]

    without_fn, footnotes = extract_footnotes(cleaned)
    # Also strip inline orphan footnote-only leftovers already extracted

    blocks = reflow_body(without_fn)

    # Drop body blocks that exactly duplicate the H1 title
    filtered = []
    for b in blocks:
        if b.lstrip("# ").strip().lower() == title.lower():
            continue
        # Drop bare "Chapter N" duplicates when title already has it
        if re.match(r"^## Chapter \d+$", b) and title.lower().startswith("chapter"):
            continue
        filtered.append(b)

    out = render(title, section, filtered, footnotes)
    path.write_text(out, encoding="utf-8")


def main() -> None:
    files = sorted(BOOK.glob("*.md"))
    done = []
    for path in files:
        if path.name in SKIP:
            continue
        normalize_file(path)
        done.append(path.name)
    print(f"normalized {len(done)} files")
    for n in done:
        print(f"  {n}")
    # Safe post-pass on already-structured markdown (mid-sentence joins, etc.)
    try:
        import sys
        from pathlib import Path as _P

        scripts_dir = str(_P(__file__).resolve().parent)
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        from polish_book_md import main as polish_main

        polish_main([])
    except Exception as exc:  # noqa: BLE001 — polish is best-effort post-pass
        print(f"note: polish pass skipped ({exc})")


if __name__ == "__main__":
    main()
