#!/usr/bin/env python3
"""Run the smallest end-to-end check for the bundled utilities."""

import tempfile
from pathlib import Path

from init_project import initialize
from build_kdp_cover import self_check as cover_self_check
from manuscript_stats import chapters
from validate_publication import self_check as publication_self_check


with tempfile.TemporaryDirectory() as temporary:
    project = Path(temporary) / "test-novel"
    created = initialize(project, "Test title", "English")
    assert created and (project / "CANON.md").exists()
    assert (project / "METADATA.yaml").exists()
    assert (project / "PRODUCTION.yaml").exists()
    assert (project / "RELEASE_MANIFEST.md").exists()
    assert (project / "FRONT_MATTER.md").exists()
    assert "Test title" in (project / "AUTHOR_COMPASS.md").read_text(encoding="utf-8")
    assert 'title: "Test title"' in (project / "METADATA.yaml").read_text(encoding="utf-8")
    chapter = project / "manuscript" / "chapter-01.md"
    chapter.write_text("# Chapter 1\n\nThree ordinary words.\n", encoding="utf-8")
    assert chapters(project / "manuscript")[0][2] == 5
    before = (project / "CANON.md").read_text(encoding="utf-8")
    initialize(project, "Replacement", "Spanish")
    assert (project / "CANON.md").read_text(encoding="utf-8") == before

publication_self_check()
cover_self_check()

print("build-novel self-check passed")
