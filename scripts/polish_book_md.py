#!/usr/bin/env python3
"""Polish already-normalized book/*.md (safe post-pass after normalize_book_md).

Fixes:
  - mid-sentence paragraph breaks from old page boundaries
  - duplicate Chapter/Step headings (keep the more specific)
  - trailing PART/Chapter bleed with no following body
  - hard-wrapped bullet continuations
  - remaining OCR leftovers (fl/fi missing, etc.)

Does not touch 00-index.md. Skips _source-cleaned.md by default (raw archive).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1] / "book"
SKIP = {"00-index.md", "_source-cleaned.md"}

HEADER_END = "Do not load other book sections unless the router names them."

# Shared / extended OCR fixes (also mirrored into normalize_book_md.py)
OCR_FIXES: list[tuple[re.Pattern[str], str]] = [
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
    (re.compile(r"\bofer\b"), "offer"),  # "I ofer some"
    (re.compile(r"\bconceptuallydriven\b"), "conceptually-driven"),
    (re.compile(r"\blongterm\b"), "long-term"),
    (re.compile(r"everybody-thinkslike-us"), "everybody-thinks-like-us"),
    (re.compile(r"\bdiferent(ly|iate|iated|iation)?\b"), r"different\1"),
    (re.compile(r"\bdifering\b"), "differing"),
    (re.compile(r"\bdifcult(y|ies)?\b"), r"difficult\1"),
    (re.compile(r"\banalysis--"), "analysis—"),
    (re.compile(r"arguments- that"), "arguments—that"),
    (re.compile(r"numbers- for"), "numbers—for"),
    (re.compile(r"DDI- I\b"), "DDI-I"),
    # wrap/OCR glitches from page breaks
    (re.compile(r"\bviewand\s+ing\b"), "viewing"),
    (re.compile(r"\bstarted viewand\b"), "started viewing"),
    (re.compile(r"\bFischof\b"), "Fischhoff"),  # common author OCR
]

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
CHAPTER_H = re.compile(r"^##\s+Chapter\s+(\d+)\s*:?\s*(.*)$", re.I)
STEP_H = re.compile(r"^##\s+Step\s+(\d+)\s*$", re.I)
PART_H = re.compile(r"^##\s+PART\s+[IVX]+\b", re.I)
FOOTNOTES_H = re.compile(r"^##\s+Footnotes\s*$", re.I)
BULLET = re.compile(r"^-\s+\S")
LIST_NUM = re.compile(r"^\d+\.\s+\S")

# Paragraph ends without sentence terminator (allow trailing footnote digits)
ENDS_SENTENCE = re.compile(r"""[.!?…]["')\]]?\d*$""")


def apply_ocr(text: str) -> str:
    for pat, repl in OCR_FIXES:
        text = pat.sub(repl, text)
    return text


def split_header(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.rstrip("\n") == HEADER_END:
            # include following blank line(s) in header
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            return "".join(lines[:j]), "".join(lines[j:])
    return "", text


def clean_heading_title(title: str) -> str:
    """Normalize messy agent/OCR chapter titles."""
    t = title.strip()
    # "## Chapter 5: , \"Do You...\"" → drop leading comma/quotes noise
    t = re.sub(r"^,\s*", "", t)
    t = re.sub(r'^["\']+|["\']+$', "", t)
    # trailing lone colon in title (Chapter N: Title:)
    t = t.rstrip(":").strip()
    # TOC dots / page numbers (front-matter)
    t = re.sub(r"\s*\.{2,}\s*\d+\s*$", "", t)
    t = re.sub(r"\s+\.{2,}.*$", "", t)
    t = re.sub(r"\s+\d{1,3}\s*$", "", t) if re.search(r"Effect\d+$", t) else t
    # "Effect127" glued page number
    t = re.sub(r"(Effect)(\d+)$", r"\1", t)
    return t.strip()


def heading_specificity(line: str) -> tuple[str, str, int]:
    """Return (kind, key, score) for duplicate detection. Higher score = keep."""
    s = line.strip()
    m = CHAPTER_H.match(s)
    if m:
        num, rest = m.group(1), clean_heading_title(m.group(2))
        # "Chapter 8: Step 8" is a weak wrapper vs "## Step 8"
        if re.match(r"^Step\s+\d+$", rest, re.I):
            return ("step", rest.split()[-1], 5)
        score = 10 + len(rest)
        if rest:
            score += 5
        return ("chapter", num, score)
    m = STEP_H.match(s)
    if m:
        return ("step", m.group(1), 20)  # prefer bare ## Step N
    if PART_H.match(s):
        return ("part", s, 10)
    m = HEADING.match(s)
    if m:
        return ("other", m.group(2).strip().lower(), 10 + len(m.group(2)))
    return ("none", s, 0)


def format_chapter_heading(line: str) -> str:
    cm = CHAPTER_H.match(line.strip())
    if not cm:
        return line
    rest = clean_heading_title(cm.group(2))
    if rest:
        return f"## Chapter {cm.group(1)}: {rest}"
    return f"## Chapter {cm.group(1)}"


def dedupe_headings(lines: list[str]) -> list[str]:
    """When consecutive headings share chapter/step identity, keep more specific."""
    # Normalize chapter heading text first so trailing ":" etc. compare equal
    normalized = [format_chapter_heading(ln) if CHAPTER_H.match(ln.strip()) else ln for ln in lines]
    out: list[str] = []
    i = 0
    while i < len(normalized):
        line = normalized[i]
        kind, key, score = heading_specificity(line)
        if kind in ("chapter", "step") and i + 1 < len(normalized):
            j = i + 1
            while j < len(normalized) and normalized[j].strip() == "":
                j += 1
            if j < len(normalized):
                k2, key2, score2 = heading_specificity(normalized[j])
                same = False
                if kind == "chapter" and k2 == "chapter" and key == key2:
                    same = True
                if kind == "step" and k2 == "step" and key == key2:
                    same = True
                # Chapter N: Step M followed by ## Step M
                if kind == "chapter" and k2 == "step":
                    rest = CHAPTER_H.match(line.strip())
                    if rest and re.match(
                        rf"^Step\s+{re.escape(key2)}$",
                        clean_heading_title(rest.group(2)),
                        re.I,
                    ):
                        same = True
                        score, score2 = 5, 20
                if kind == "step" and k2 == "chapter":
                    rest = CHAPTER_H.match(normalized[j].strip())
                    if rest and re.match(
                        rf"^Step\s+{re.escape(key)}$",
                        clean_heading_title(rest.group(2)),
                        re.I,
                    ):
                        same = True
                        score, score2 = 20, 5
                if same:
                    # Prefer higher score; on tie prefer longer (more specific) title
                    a, b = line, normalized[j]
                    if score2 > score or (score2 == score and len(b) > len(a)):
                        keep = b
                    else:
                        keep = a
                    out.append(keep)
                    i = j + 1
                    continue
        out.append(line)
        i += 1
    return out


def is_structural_heading(line: str) -> bool:
    s = line.strip()
    return bool(
        CHAPTER_H.match(s)
        or STEP_H.match(s)
        or PART_H.match(s)
        or FOOTNOTES_H.match(s)
        or (HEADING.match(s) and s.startswith("## "))
    )


def remove_section_bleed(lines: list[str]) -> list[str]:
    """Drop PART/Chapter headings that sit with no body before Footnotes or EOF.

    Also drop a PART heading immediately before another Chapter heading when
    the PART has no body (composite agent files spanning parts).
    """
    # Pass 1: remove headings immediately before ## Footnotes / EOF with only blanks
    out = list(lines)
    changed = True
    while changed:
        changed = False
        # find footnotes index or end
        fn_idx = None
        for i, ln in enumerate(out):
            if FOOTNOTES_H.match(ln.strip()):
                fn_idx = i
                break
        end = fn_idx if fn_idx is not None else len(out)
        # walk backward from end-1 skipping blanks
        k = end - 1
        while k >= 0 and out[k].strip() == "":
            k -= 1
        if k < 0:
            break
        s = out[k].strip()
        if PART_H.match(s) or CHAPTER_H.match(s):
            # ensure nothing but blanks between this heading and end marker
            # (heading is last non-blank before footnotes/EOF)
            del out[k:end]
            # re-add single blank before footnotes if needed
            if fn_idx is not None:
                # footnotes shifted
                new_fn = None
                for i, ln in enumerate(out):
                    if FOOTNOTES_H.match(ln.strip()):
                        new_fn = i
                        break
                if new_fn is not None and (new_fn == 0 or out[new_fn - 1].strip() != ""):
                    out.insert(new_fn, "")
            changed = True
            continue
        break

    # Pass 2: PART heading with no body before next Chapter/PART/Footnotes
    i = 0
    rebuilt: list[str] = []
    while i < len(out):
        s = out[i].strip()
        if PART_H.match(s):
            j = i + 1
            while j < len(out) and out[j].strip() == "":
                j += 1
            if j >= len(out):
                # trailing PART — drop
                i = j
                continue
            nxt = out[j].strip()
            if (
                CHAPTER_H.match(nxt)
                or PART_H.match(nxt)
                or FOOTNOTES_H.match(nxt)
                or STEP_H.match(nxt)
            ):
                # bleed into next section — drop PART
                i = j
                continue
        rebuilt.append(out[i])
        i += 1
    return rebuilt


def join_hardwrapped_bullets(lines: list[str]) -> list[str]:
    """Join bullet continuation lines onto the bullet."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if BULLET.match(line.strip()) or (
            line.strip().startswith("- ") and len(line.strip()) > 2
        ):
            text = line.rstrip()
            i += 1
            while i < len(lines):
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    # peek past blank: lowercase continuation still joins
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j >= len(lines):
                        break
                    peek = lines[j].strip()
                    if (
                        BULLET.match(peek)
                        or LIST_NUM.match(peek)
                        or is_structural_heading(peek)
                        or HEADING.match(peek)
                    ):
                        break
                    # Only join across blank if previous doesn't end a sentence
                    # and peek starts lowercase (true wrap), OR prev ends with
                    # hyphenated mid-phrase words like "of"/"rather"/"and"
                    if not ends_as_sentence(text) and (
                        peek[:1].islower()
                        or text.rstrip().endswith(
                            (
                                "rather",
                                "of",
                                "or",
                                "and",
                                "the",
                                "a",
                                "an",
                                "to",
                                "for",
                                "with",
                                "from",
                                "in",
                                "on",
                                "at",
                                "by",
                                "as",
                                "that",
                                "which",
                                "who",
                                "their",
                                "its",
                            )
                        )
                    ):
                        text = text + " " + peek
                        i = j + 1
                        continue
                    break
                if (
                    BULLET.match(ns)
                    or LIST_NUM.match(ns)
                    or is_structural_heading(ns)
                    or HEADING.match(ns)
                ):
                    break
                # same-paragraph wrap (no blank between)
                if not ends_as_sentence(text) or ns[:1].islower():
                    text = text + " " + ns
                    i += 1
                    continue
                break
            out.append(text)
            continue
        out.append(line)
        i += 1
    return out


def ends_as_sentence(s: str) -> bool:
    """True if text ends with sentence terminator (not a decimal like .70)."""
    s = s.rstrip()
    if not s:
        return False
    # decimals: .70 or 0.70 or x .70
    if re.search(r"(?:^|[\s=x×*/])\.\d+$", s) or re.search(r"\d\.\d+$", s):
        return False
    return bool(ENDS_SENTENCE.search(s))


def ends_incomplete(para: str) -> bool:
    """True if paragraph likely continues (page-break mid-sentence)."""
    s = para.rstrip()
    if not s:
        return False
    last_line = s.split("\n")[-1].strip()
    if is_structural_heading(last_line) or HEADING.match(last_line):
        return False
    # Single-line list/bullet that already ends a sentence is complete;
    # multi-line blocks are judged by their ending (list+prose glued together).
    if "\n" not in s and (BULLET.match(s) or LIST_NUM.match(s)):
        if ends_as_sentence(s):
            return False
        last = s[-1]
        return last.isalnum() or last in ",;:—–-\"'"
    # Footnote markers glued after punctuation (judgment.85) count as complete.
    if ends_as_sentence(s):
        return False
    last = s[-1]
    if last.isalnum() or last in ",;:—–-\"'":
        return True
    return False


def starts_continuation(para: str) -> bool:
    s = para.lstrip()
    if not s:
        return False
    if is_structural_heading(s) or HEADING.match(s):
        return False
    if BULLET.match(s) or LIST_NUM.match(s):
        return False
    # lowercase start = clear continuation
    if s[0].islower():
        return True
    return False


DANGLING_END = re.compile(
    r"(?i)\b(?:the|a|an|and|or|but|of|to|for|with|from|in|on|at|by|as|"
    r"that|which|who|whom|whose|their|its|his|her|our|your|than|"
    r"rather|into|onto|upon|about|over|under|between|through|"
    r"without|within|whether|while|when|where|because|if|unless|"
    r"although|though|since|until|after|before|during|via|per|"
    r"is|are|was|were|be|been|being|have|has|had|do|does|did|"
    r"can|could|will|would|shall|should|may|might|must|need|"
    r"not|no|so|such|these|those|this|these)\s*$"
)


def join_mid_sentence_paras(text: str) -> str:
    """Join paragraphs split mid-sentence by old page boundaries."""
    parts = re.split(r"\n\n+", text)
    if not parts:
        return text
    out: list[str] = [parts[0]]
    for p in parts[1:]:
        prev = out[-1]
        ps = p.lstrip()
        prev_last = prev.rstrip().split("\n")[-1].strip()

        # Heading followed by lowercase fragment → extend heading title
        if (
            (is_structural_heading(prev_last) or HEADING.match(prev_last))
            and ps
            and ps[0].islower()
            and not is_structural_heading(ps)
            and not HEADING.match(ps)
            and len(ps.split()) <= 24
        ):
            if CHAPTER_H.match(prev_last) or prev_last.startswith("## "):
                frag = ps.split("\n")[0].strip().rstrip(".")
                lines = prev.rstrip().split("\n")
                lines[-1] = lines[-1].rstrip() + " " + frag
                rest = "\n".join(ps.split("\n")[1:]).strip()
                out[-1] = "\n".join(lines)
                if rest:
                    out.append(rest)
                continue

        if ends_incomplete(prev) and starts_continuation(p):
            out[-1] = prev.rstrip() + " " + ps
            continue
        # "Look at Figure" + "3. What do you see..." (figure number, not a list)
        if ends_incomplete(prev) and re.search(
            r"\b(?:Figure|Chapter|Part|Step|Table)\s*$", prev.rstrip(), re.I
        ):
            if re.match(r"^\d+[.:]?\s+\S", ps) or re.match(r"^\d+\s*$", ps.split("\n")[0]):
                out[-1] = prev.rstrip() + " " + ps
                continue
        # Incomplete + uppercase next: only when prev ends on a dangling function word
        if (
            ends_incomplete(prev)
            and DANGLING_END.search(prev.rstrip())
            and ps
            and not is_structural_heading(ps)
            and not HEADING.match(ps)
            and not BULLET.match(ps)
            and not LIST_NUM.match(ps)
            and len(prev.split()) >= 8
        ):
            out[-1] = prev.rstrip() + " " + ps
            continue
        out.append(p)
    return "\n\n".join(out)


def collapse_blank_lines(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip() + "\n"


def polish_body(body: str) -> str:
    body = apply_ocr(body)
    lines = body.splitlines()
    lines = dedupe_headings(lines)
    lines = remove_section_bleed(lines)
    lines = join_hardwrapped_bullets(lines)
    # Also join hard-wrapped numbered list items similarly
    lines = join_hardwrapped_numbered(lines)
    text = "\n".join(lines)
    text = join_mid_sentence_paras(text)
    # second OCR pass after joins (e.g. viewand + ing already fixed as phrase)
    text = apply_ocr(text)
    text = collapse_blank_lines(text)
    return text


def join_hardwrapped_numbered(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if LIST_NUM.match(line.strip()):
            text = line.rstrip()
            i += 1
            while i < len(lines):
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j >= len(lines):
                        break
                    peek = lines[j].strip()
                    if (
                        LIST_NUM.match(peek)
                        or BULLET.match(peek)
                        or is_structural_heading(peek)
                    ):
                        break
                    if not ends_as_sentence(text) and peek[:1].islower():
                        text = text + " " + peek
                        i = j + 1
                        continue
                    break
                if (
                    LIST_NUM.match(ns)
                    or BULLET.match(ns)
                    or is_structural_heading(ns)
                    or HEADING.match(ns)
                ):
                    break
                if not ends_as_sentence(text) or ns[:1].islower():
                    text = text + " " + ns
                    i += 1
                    continue
                break
            out.append(text)
            continue
        out.append(line)
        i += 1
    return out


def polish_file(path: Path) -> dict[str, int]:
    raw = path.read_text(encoding="utf-8")
    header, body = split_header(raw)
    if not header:
        # no standard header — polish whole file carefully
        new_body = polish_body(raw)
        if new_body != raw:
            path.write_text(new_body, encoding="utf-8")
        return {"changed": int(new_body != raw)}
    new_body = polish_body(body)
    out = header + new_body
    if not out.endswith("\n"):
        out += "\n"
    changed = out != raw
    if changed:
        path.write_text(out, encoding="utf-8")
    return {"changed": int(changed)}


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    include_source = "--include-source" in argv
    paths = [Path(a) for a in argv if not a.startswith("-")]
    if not paths:
        paths = sorted(BOOK.glob("*.md"))
    done = []
    skipped = []
    for path in paths:
        if path.name == "00-index.md":
            skipped.append(path.name)
            continue
        if path.name == "_source-cleaned.md" and not include_source:
            skipped.append(path.name)
            continue
        polish_file(path)
        done.append(path.name)
    print(f"polished {len(done)} files (skipped {len(skipped)}: {', '.join(skipped)})")
    for n in done:
        print(f"  {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
