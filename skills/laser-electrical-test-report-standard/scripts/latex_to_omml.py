#!/usr/bin/env python3
"""Convert LaTeX math to editable Word OMML through Pandoc."""

from __future__ import annotations

import copy
import shutil
import subprocess
import tempfile
import zipfile
from functools import lru_cache
from pathlib import Path

from lxml import etree


MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"m": MATH_NS}


def require_pandoc() -> str:
    executable = shutil.which("pandoc")
    if executable is None:
        raise RuntimeError("Pandoc is required for LaTeX-to-OMML conversion but was not found on PATH.")
    return executable


@lru_cache(maxsize=256)
def _latex_xml(latex: str) -> bytes:
    if not latex.strip():
        raise ValueError("LaTeX expression must not be empty.")
    pandoc = require_pandoc()
    markdown = f"$${latex}$$\n"
    with tempfile.TemporaryDirectory(prefix="laser_latex_omml_") as directory:
        output = Path(directory) / "formula.docx"
        completed = subprocess.run(
            [pandoc, "--from=markdown+tex_math_dollars", "--to=docx", "--output", str(output)],
            input=markdown,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Pandoc failed to convert LaTeX: {completed.stderr.strip()}")
        with zipfile.ZipFile(output) as archive:
            document = etree.fromstring(archive.read("word/document.xml"))
    items = document.xpath("//m:oMath", namespaces=NS)
    if len(items) != 1:
        raise RuntimeError(f"Expected one OMML expression, found {len(items)} for: {latex}")
    return etree.tostring(items[0])


def latex_to_omml(latex: str):
    """Return a detached m:oMath element suitable for inline or display use."""
    return copy.deepcopy(etree.fromstring(_latex_xml(latex)))


def latex_to_display_omml(latex: str):
    """Return an m:oMathPara element containing professional Word math."""
    wrapper = etree.Element(f"{{{MATH_NS}}}oMathPara")
    wrapper.append(latex_to_omml(latex))
    return wrapper

