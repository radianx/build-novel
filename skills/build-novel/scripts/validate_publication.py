#!/usr/bin/env python3
"""Validate structural publication basics for EPUB and PDF artifacts."""

import argparse
import posixpath
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile


DRAFT_MARKERS = ("BORRADOR DE IMPRESIÓN", "[Not written]", "{{TITLE}}", "{{LANGUAGE}}", "{{DATE}}")
PAPER_MULTIPLIERS = {"white": 0.002252, "cream": 0.0025, "groundwood": 0.00235}


def parse_trim(value: str) -> tuple[float, float]:
    try:
        width, height = (float(part) for part in value.lower().split("x", 1))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("trim must look like 6x9") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("trim dimensions must be positive")
    return width, height


def expected_pdf_size(profile: str, trim: tuple[float, float], pages: int | None, paper: str | None) -> tuple[float, float] | None:
    width, height = trim
    if profile == "print-no-bleed":
        return width * 72, height * 72
    if profile == "print-bleed":
        return (width + 0.125) * 72, (height + 0.25) * 72
    if profile == "cover-wrap" and pages and paper:
        pages += pages % 2
        return (2 * width + pages * PAPER_MULTIPLIERS[paper] + 0.25) * 72, (height + 0.25) * 72
    return None


def command_output(command: list[str]) -> tuple[str, str | None]:
    executable = shutil.which(command[0])
    if not executable:
        return "", f"{command[0]} not installed; check skipped"
    result = subprocess.run([executable, *command[1:]], capture_output=True, text=True)
    return result.stdout, (result.stderr.strip() or f"{command[0]} failed") if result.returncode else None


def validate_epub(path: Path) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    try:
        with ZipFile(path) as archive:
            names = archive.namelist()
            bad = archive.testzip()
            if bad:
                errors.append(f"corrupt ZIP member: {bad}")
            if not names or names[0] != "mimetype":
                errors.append("mimetype is not the first ZIP entry")
            elif archive.getinfo("mimetype").compress_type != ZIP_STORED:
                errors.append("mimetype is compressed")
            if "mimetype" not in names or archive.read("mimetype") != b"application/epub+zip":
                errors.append("invalid EPUB mimetype")
            if "META-INF/container.xml" not in names:
                return errors + ["missing META-INF/container.xml"], warnings

            container = ET.fromstring(archive.read("META-INF/container.xml"))
            rootfile = container.find("{*}rootfiles/{*}rootfile")
            opf_name = rootfile.get("full-path") if rootfile is not None else None
            if not opf_name or opf_name not in names:
                return errors + ["package document is missing"], warnings
            package = ET.fromstring(archive.read(opf_name))
            for field in ("title", "creator", "language"):
                if not (package.findtext(f".//{{*}}{field}") or "").strip():
                    errors.append(f"missing dc:{field}")

            manifest = {item.get("id"): item for item in package.findall(".//{*}manifest/{*}item")}
            nav_items = [item for item in manifest.values() if "nav" in (item.get("properties") or "").split()]
            if len(nav_items) != 1:
                errors.append("manifest must contain exactly one navigation document")
            for item in manifest.values():
                href = item.get("href")
                target = posixpath.normpath(posixpath.join(posixpath.dirname(opf_name), href or ""))
                if not href or target not in names:
                    errors.append(f"missing manifest resource: {href or item.get('id')}")
            for itemref in package.findall(".//{*}spine/{*}itemref"):
                if itemref.get("idref") not in manifest:
                    errors.append(f"unknown spine idref: {itemref.get('idref')}")

            combined_text = []
            for name in (name for name in names if name.endswith((".xhtml", ".html"))):
                try:
                    root = ET.fromstring(archive.read(name))
                except ET.ParseError as exc:
                    errors.append(f"invalid XHTML {name}: {exc}")
                    continue
                combined_text.append("".join(root.itertext()))
                for element in root.iter():
                    if element.tag.endswith("}img"):
                        alt = element.get("alt")
                        decorative = element.get("role") in {"presentation", "none"} or element.get("aria-hidden") == "true"
                        if alt is None or (not alt.strip() and not decorative):
                            errors.append(f"image without useful alt text: {name}")
                    for attribute in ("href", "src"):
                        value = element.get(attribute)
                        if not value or "://" in value or value.startswith(("#", "data:", "mailto:")):
                            continue
                        target = posixpath.normpath(posixpath.join(posixpath.dirname(name), value.split("#")[0]))
                        if target not in names:
                            errors.append(f"broken reference in {name}: {value}")
            text = "\n".join(combined_text)
            for marker in DRAFT_MARKERS:
                if marker in text:
                    errors.append(f"draft marker found: {marker}")
    except (OSError, ET.ParseError) as exc:
        errors.append(str(exc))

    epubcheck = shutil.which("epubcheck")
    if epubcheck and not errors:
        result = subprocess.run([epubcheck, str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append("EPUBCheck failed:\n" + (result.stdout + result.stderr).strip())
    elif not epubcheck:
        warnings.append("EPUBCheck not installed; internal structural checks only")
    return errors, warnings


def validate_pdf(
    path: Path,
    profile: str,
    trim: tuple[float, float] = (6, 9),
    pages: int | None = None,
    paper: str | None = None,
    require_final_recto: bool = False,
) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        return ["pdfinfo is required to validate PDF files"], warnings
    result = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True)
    if result.returncode:
        return [result.stderr.strip() or "pdfinfo failed"], warnings
    fields = {}
    for line in result.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    required_fields = ("Pages", "Page size") if profile == "cover-wrap" else ("Title", "Author", "Pages", "Page size")
    for field in required_fields:
        if not fields.get(field):
            errors.append(f"missing PDF metadata: {field}")
    if profile != "cover-wrap" and not fields.get("Subject"):
        warnings.append("PDF Subject/series metadata is empty")
    if profile == "digital":
        if fields.get("Tagged", "").lower() != "yes":
            errors.append("digital PDF is not tagged")
        if b"/Outlines" not in path.read_bytes():
            errors.append("digital PDF has no navigation outline")
    actual_pages = int(fields.get("Pages", "0") or 0)
    if profile == "cover-wrap" and actual_pages != 1:
        errors.append(f"cover wrap must be one page, found {actual_pages}")
    if require_final_recto and actual_pages % 2 != 1:
        errors.append(f"final page is verso: interior has {actual_pages} pages")

    expected = expected_pdf_size(profile, trim, pages, paper)
    if expected:
        detailed = subprocess.run([pdfinfo, "-f", "1", "-l", str(actual_pages), str(path)], capture_output=True, text=True)
        sizes = [(float(width), float(height)) for width, height in re.findall(r"(?:Page\s+\d+\s+size|Page size):\s*([\d.]+) x ([\d.]+) pts", detailed.stdout)]
        if not sizes:
            errors.append("could not read PDF page dimensions")
        for number, actual in enumerate(sizes, 1):
            if any(abs(value - target) > 0.2 for value, target in zip(actual, expected)):
                errors.append(f"page {number} is {actual[0]:g}x{actual[1]:g} pt; expected {expected[0]:g}x{expected[1]:g} pt")
                break

    fonts, font_warning = command_output(["pdffonts", str(path)])
    if font_warning:
        warnings.append(font_warning)
    else:
        for line in fonts.splitlines()[2:]:
            match = re.search(r"\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line)
            if match and match.group(1) == "no":
                errors.append("PDF contains a font that is not embedded")
                break

    images, image_warning = command_output(["pdfimages", "-list", str(path)])
    if image_warning:
        warnings.append(image_warning)
    elif profile in {"print", "print-no-bleed", "print-bleed", "cover-wrap"}:
        for line in images.splitlines()[2:]:
            columns = line.split()
            if len(columns) >= 14 and columns[0].isdigit() and columns[12].isdigit() and columns[13].isdigit():
                if min(int(columns[12]), int(columns[13])) < 300:
                    warnings.append(f"image on page {columns[0]} is below 300 effective DPI")
                    break

    extracted, text_warning = command_output(["pdftotext", str(path), "-"])
    if text_warning:
        warnings.append(text_warning)
    else:
        for marker in DRAFT_MARKERS:
            if marker in extracted:
                errors.append(f"draft marker found: {marker}")
    return errors, warnings


def validate_kindle_cover(path: Path) -> tuple[list[str], list[str]]:
    try:
        from PIL import Image
        with Image.open(path) as image:
            errors = []
            if image.mode != "RGB":
                errors.append(f"Kindle cover must be RGB, found {image.mode}")
            if image.size != (1600, 2560):
                errors.append(f"Kindle cover must be 1600x2560 px, found {image.width}x{image.height}")
            return errors, []
    except (ImportError, OSError) as exc:
        return [str(exc)], []


def self_check() -> None:
    assert expected_pdf_size("print-no-bleed", (6, 9), None, None) == (432, 648)
    assert expected_pdf_size("print-bleed", (6, 9), None, None) == (441, 666)
    cover = expected_pdf_size("cover-wrap", (6, 9), 101, "groundwood")
    assert cover and round(cover[0], 3) == round((12.25 + 102 * 0.00235) * 72, 3)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "META-INF").mkdir()
        (root / "EPUB").mkdir()
        (root / "mimetype").write_text("application/epub+zip", encoding="ascii")
        (root / "META-INF/container.xml").write_text('<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', encoding="utf-8")
        (root / "EPUB/chapter.xhtml").write_text('<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>One</title></head><body><h1>One</h1></body></html>', encoding="utf-8")
        (root / "EPUB/nav.xhtml").write_text('<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Contents</title></head><body><nav><a href="chapter.xhtml">One</a></nav></body></html>', encoding="utf-8")
        (root / "EPUB/package.opf").write_text('<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Test</dc:title><dc:creator>Author</dc:creator><dc:language>en</dc:language></metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="chapter" href="chapter.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="chapter"/></spine></package>', encoding="utf-8")
        epub = root / "test.epub"
        with ZipFile(epub, "w") as archive:
            archive.write(root / "mimetype", "mimetype", compress_type=ZIP_STORED)
            for name in ("META-INF/container.xml", "EPUB/package.opf", "EPUB/nav.xhtml", "EPUB/chapter.xhtml"):
                archive.write(root / name, name)
        errors, _ = validate_epub(epub)
        assert not errors, errors
        from PIL import Image
        kindle = root / "kindle.jpg"
        Image.new("RGB", (1600, 2560)).save(kindle)
        errors, _ = validate_kindle_cover(kindle)
        assert not errors, errors
    print("validate_publication self-check passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", nargs="*", type=Path)
    parser.add_argument("--profile", choices=("auto", "print", "digital", "print-no-bleed", "print-bleed", "cover-wrap", "kindle-cover"), default="auto")
    parser.add_argument("--trim", type=parse_trim, default=(6, 9))
    parser.add_argument("--pages", type=int)
    parser.add_argument("--paper", choices=tuple(PAPER_MULTIPLIERS))
    parser.add_argument("--require-final-recto", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return
    if not args.artifacts:
        parser.error("provide at least one PDF or EPUB")
    if args.profile == "cover-wrap" and (args.pages is None or args.paper is None):
        parser.error("cover-wrap requires --pages and --paper")
    failed = False
    for path in args.artifacts:
        if path.suffix.lower() == ".epub":
            errors, warnings = validate_epub(path)
        elif path.suffix.lower() == ".pdf":
            profile = "print" if args.profile == "auto" else args.profile
            if profile == "kindle-cover":
                errors, warnings = ["kindle-cover requires a JPEG or PNG image"], []
            else:
                errors, warnings = validate_pdf(path, profile, args.trim, args.pages, args.paper, args.require_final_recto)
        elif path.suffix.lower() in {".jpg", ".jpeg", ".png"} and args.profile == "kindle-cover":
            errors, warnings = validate_kindle_cover(path)
        else:
            errors, warnings = ["unsupported file type"], []
        print(f"{path}: {'FAIL' if errors else 'OK'}")
        for warning in warnings:
            print(f"  warning: {warning}")
        for error in errors:
            print(f"  error: {error}")
        failed |= bool(errors)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
