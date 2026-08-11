#!/usr/bin/env python3
"""Fix remaining book structure: subtitles into headings, split long paras, clean TOC."""

from __future__ import annotations

import re
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1] / "book"
SKIP = {"00-index.md", "_source-cleaned.md"}
HEADER_END = "Do not load other book sections unless the router names them."
PDF = "https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf"
SOURCE = "Richards J. Heuer, Jr., *Psychology of Intelligence Analysis* (CSI/CIA, 1999)."

# Subtitle fragments that belong in the preceding ## Chapter heading
KNOWN_SUBTITLES = [
    "What Is There To Be Seen?",
    "What We Know?",
    "Transcending the Limits of Incomplete Information",
    "Intelligence Reporting",
    "Reporting",
]

# Soft-split long paragraphs after these blurb endings (chapter abstract → body)
BLURB_SPLIT = re.compile(
    r"(intelligence analysis\.|intelligence analysts\.|following chapters\.|"
    r"intelligence reporting\.|to be tested by collecting and presenting evidence\.)"
    r"(\d{0,3})\s+(?=[A-Z\"])"
)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“])")
MAX_PARA = 520  # chars — split longer prose at sentence boundaries


def split_header(text: str) -> tuple[str, str]:
    idx = text.find(HEADER_END)
    if idx < 0:
        return "", text
    end = idx + len(HEADER_END)
    return text[:end].rstrip(), text[end:].lstrip("\n")


def absorb_subtitles(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## Chapter"):
            # look ahead past blanks for subtitle-leading paragraph
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines) and not lines[j].startswith("#"):
                para = lines[j].strip()
                absorbed = False
                for sub in sorted(KNOWN_SUBTITLES, key=len, reverse=True):
                    if para == sub or para.startswith(sub + " ") or para.startswith(sub + "."):
                        # merge into heading if not already present
                        if sub.rstrip("?") not in line and sub not in line:
                            # special: "Reporting" alone after "Evaluation of"
                            if sub == "Reporting" and line.rstrip().endswith("Evaluation of"):
                                line = line.rstrip() + " Intelligence Reporting"
                            elif sub == "Intelligence Reporting" and "Intelligence Reporting" not in line:
                                if line.rstrip().endswith("Evaluation of"):
                                    line = line.rstrip() + " Intelligence Reporting"
                                else:
                                    line = line.rstrip() + ": " + sub
                            elif sub not in line:
                                # complete truncated titles
                                if line.endswith("Why Can't We See") and sub.startswith("What Is"):
                                    line = line + " " + sub
                                elif line.endswith("How Do We Remember") and sub.startswith("What We"):
                                    line = line.rstrip("?") + " " + sub
                                elif "Strategies for Analytical Judgment" in line and sub.startswith("Transcending"):
                                    line = line.rstrip() + ": " + sub
                                else:
                                    line = line.rstrip() + " " + sub
                        # strip subtitle from paragraph
                        rest = para[len(sub) :].lstrip(" .")
                        out.append(line)
                        out.append("")
                        if rest:
                            out.append(rest)
                        i = j + 1
                        absorbed = True
                        break
                if absorbed:
                    continue
            out.append(line)
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def split_long_paragraph(para: str) -> list[str]:
    if len(para) <= MAX_PARA or para.startswith("#") or para.startswith("- ") or re.match(r"^\d+\.\s", para):
        return [para]

    # Prefer split after chapter blurb / abstract
    m = BLURB_SPLIT.search(para)
    if m and m.end() < len(para) - 40:
        a = para[: m.end(1)] + (m.group(2) or "")
        b = para[m.end() :].lstrip()
        return split_long_paragraph(a.strip()) + split_long_paragraph(b)

    # Split at sentence boundaries into chunks ~MAX_PARA
    parts = SENTENCE_SPLIT.split(para)
    if len(parts) <= 1:
        return [para]
    chunks: list[str] = []
    buf = ""
    for sent in parts:
        sent = sent.strip()
        if not sent:
            continue
        if not buf:
            buf = sent
        elif len(buf) + 1 + len(sent) <= MAX_PARA:
            buf = buf + " " + sent
        else:
            chunks.append(buf)
            buf = sent
    if buf:
        chunks.append(buf)
    return chunks or [para]


def split_body_paragraphs(body: str) -> str:
    blocks = re.split(r"\n\s*\n", body)
    out: list[str] = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("#") or block.startswith("- ") or re.match(r"^\d+\.\s", block):
            # multi-line list blocks: leave
            out.append(block)
            continue
        # single-line heading already handled
        for piece in split_long_paragraph(block):
            out.append(piece)
    return "\n\n".join(out) + "\n"


def fix_broken_headings(body: str) -> str:
    """Fix known mangled headings like Chapter 5 glued to prose."""
    body = re.sub(
        r"(## Chapter 5: Do You Really Need More Information\?)\s+explicit so that",
        r"\1\n\n…explicit so that",  # mark — better drop orphan fragment
        body,
    )
    # Remove orphan fragment lines that start with lowercase after bad glue
    body = re.sub(
        r"## Chapter 5: Do You Really Need More Information\?\n\n…explicit so that[^\n]*\n\n",
        "## Chapter 5: Do You Really Need More Information?\n\n",
        body,
    )
    # ch13: ## Chapter 13: ... Intelligence\n\nReporting Evaluations → merge
    body = re.sub(
        r"(## Chapter 13: Hindsight Biases in Evaluation of Intelligence)\n\nReporting Evaluations",
        r"\1 Reporting\n\nEvaluations",
        body,
    )
    body = re.sub(
        r"(## Chapter 13: Hindsight Biases in Evaluation of Intelligence Reporting)\n\nEvaluations",
        r"\1\n\nEvaluations",
        body,
    )
    return body


FRONT_MATTER = f"""# Front Matter / Table of Contents

Source: {SOURCE}
PDF: {PDF}
Section: front-matter

Do not load other book sections unless the router names them.

# Psychology of Intelligence Analysis

**Richards J. Heuer, Jr.**

CENTER for the STUDY of INTELLIGENCE  
Central Intelligence Agency  
1999

This book was prepared primarily for the use of US Government officials, and the format, coverage, and content were designed to meet their specific requirements.

Because this book is now out of print, this Portable Document File (PDF) is formatted for two-sided printing to facilitate desktop publishing. It may be used by US Government agencies to make copies for government purposes and by non-governmental organizations to make copies for educational purposes. Because this book may be subject to copyright restriction, copies may not be made for any commercial purpose.

This book will be available at www.odci.gov/csi.

All statements of fact, opinion, or analysis expressed in the main text of this book are those of the author. Similarly, all such statements in the Forward and the Introduction are those of the respective authors of those sections. Such statements of fact, opinion, or analysis do not necessarily reflect the official positions or views of the Central Intelligence Agency or any other component of the US Intelligence Community. Nothing in the contents of this book should be construed as asserting or implying US Government endorsement of factual statements or interpretations.

ISBN 1 929667-00-0

Originally published in 1999.

## Contents

| Section | Page |
|---|---:|
| Author's Preface | vi |
| Foreword | ix |
| Introduction | xiii |
| Chapter 1: Thinking About Thinking | 1 |
| Chapter 2: Perception: Why Can't We See What Is There To Be Seen? | 7 |
| Chapter 3: Memory: How Do We Remember What We Know? | 17 |
| Chapter 4: Strategies for Analytical Judgment: Transcending the Limits of Incomplete Information | 31 |
| Chapter 5: Do You Really Need More Information? | 51 |
| Chapter 6: Keeping an Open Mind | 65 |
| Chapter 7: Structuring Analytical Problems | 85 |
| Chapter 8: Analysis of Competing Hypotheses | 95 |
| Chapter 9: What Are Cognitive Biases? | 111 |
| Chapter 10: Biases in Evaluation of Evidence | 115 |
| Chapter 11: Biases in Perception of Cause and Effect | 127 |
| Chapter 12: Biases in Estimating Probabilities | 147 |
| Chapter 13: Hindsight Biases in Evaluation of Intelligence Reporting | 161 |
| Chapter 14: Improving Intelligence Analysis | 173 |
"""


def process_file(path: Path) -> None:
    if path.name == "front-matter.md":
        path.write_text(FRONT_MATTER, encoding="utf-8")
        return

    text = path.read_text(encoding="utf-8")
    header, body = split_header(text)
    if not header:
        return
    body = absorb_subtitles(body)
    body = fix_broken_headings(body)
    body = split_body_paragraphs(body)
    # tidy blank lines
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    path.write_text(header + "\n\n" + body, encoding="utf-8")


def main() -> None:
    n = 0
    for path in sorted(BOOK.glob("*.md")):
        if path.name in SKIP:
            continue
        process_file(path)
        n += 1
        print(path.name)
    print(f"structure-fixed {n} files")


if __name__ == "__main__":
    main()
