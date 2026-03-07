"""Tests that enforce TE-Learn content conventions.

These tests scan the content/ directory and validate that all markdown files
follow the agreed-upon conventions for slugs, frontmatter, and structure.
"""

from pathlib import Path

import pytest
import yaml

CONTENT_DIR = Path(__file__).parent.parent / "content"
VALID_STATUSES = {"draft", "review", "published"}
VALID_BLOOMS = {"Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"}
VALID_EDITIONS = {"te3_desktop", "te3_business", "te3_enterprise"}
MAX_SLUG_WORDS = 2


def _all_content_dirs() -> list[Path]:
    """Return all directories under content/ (groups and TOs)."""
    return [d for d in CONTENT_DIR.rglob("*") if d.is_dir() and d.name != "media"]


def _all_eo_files() -> list[Path]:
    """Return all EO markdown files (not _index.md)."""
    return [
        f
        for f in CONTENT_DIR.rglob("*.md")
        if f.name != "_index.md" and f.suffix == ".md"
    ]


def _all_index_files() -> list[Path]:
    """Return all _index.md files."""
    return list(CONTENT_DIR.rglob("_index.md"))


def _parse_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm_text, _ = text.split("---", 2)
    return yaml.safe_load(fm_text) or {}


# --- Slug conventions ---


class TestSlugConventions:
    """Folder and file slugs must be at most 2 words (kebab-case)."""

    @pytest.mark.parametrize("directory", _all_content_dirs(), ids=lambda d: d.name)
    def test_folder_slug_max_two_words(self, directory: Path) -> None:
        slug = directory.name
        word_count = len(slug.split("-"))
        assert word_count <= MAX_SLUG_WORDS, (
            f"Folder slug '{slug}' has {word_count} words (max {MAX_SLUG_WORDS}). "
            f"Path: {directory.relative_to(CONTENT_DIR)}"
        )

    @pytest.mark.parametrize("eo_file", _all_eo_files(), ids=lambda f: f.stem)
    def test_eo_uid_matches_filename(self, eo_file: Path) -> None:
        fm = _parse_frontmatter(eo_file)
        if "uid" in fm:
            assert fm["uid"] == eo_file.stem, (
                f"uid '{fm['uid']}' does not match filename '{eo_file.stem}'"
            )


# --- Frontmatter conventions ---


class TestEOFrontmatter:
    """EO files must have required frontmatter fields with valid values."""

    REQUIRED_FIELDS = {"uid", "title", "status", "author", "updated"}

    @pytest.mark.parametrize("eo_file", _all_eo_files(), ids=lambda f: f.stem)
    def test_required_fields_present(self, eo_file: Path) -> None:
        fm = _parse_frontmatter(eo_file)
        missing = self.REQUIRED_FIELDS - set(fm.keys())
        assert not missing, (
            f"{eo_file.name} missing required frontmatter: {missing}"
        )

    @pytest.mark.parametrize("eo_file", _all_eo_files(), ids=lambda f: f.stem)
    def test_status_is_valid(self, eo_file: Path) -> None:
        fm = _parse_frontmatter(eo_file)
        status = fm.get("status")
        if status is not None:
            assert status in VALID_STATUSES, (
                f"{eo_file.name} has invalid status '{status}'. "
                f"Must be one of: {VALID_STATUSES}"
            )

    @pytest.mark.parametrize("eo_file", _all_eo_files(), ids=lambda f: f.stem)
    def test_blooms_level_is_valid(self, eo_file: Path) -> None:
        fm = _parse_frontmatter(eo_file)
        blooms = fm.get("blooms_level")
        if blooms is not None:
            assert blooms in VALID_BLOOMS, (
                f"{eo_file.name} has invalid blooms_level '{blooms}'. "
                f"Must be one of: {VALID_BLOOMS}"
            )

    @pytest.mark.parametrize("eo_file", _all_eo_files(), ids=lambda f: f.stem)
    def test_edition_minimum_is_valid(self, eo_file: Path) -> None:
        fm = _parse_frontmatter(eo_file)
        edition = fm.get("edition_minimum")
        if edition is not None:
            assert edition in VALID_EDITIONS, (
                f"{eo_file.name} has invalid edition_minimum '{edition}'. "
                f"Must be one of: {VALID_EDITIONS}"
            )


# --- Structure conventions ---


class TestStructureConventions:
    """Content directories must follow Group -> TO -> EO structure."""

    @pytest.mark.parametrize(
        "index_file", _all_index_files(), ids=lambda f: str(f.parent.name)
    )
    def test_index_files_have_uid(self, index_file: Path) -> None:
        fm = _parse_frontmatter(index_file)
        assert "uid" in fm, (
            f"_index.md in {index_file.parent.name}/ is missing uid in frontmatter"
        )

    def test_every_to_folder_has_media_dir(self) -> None:
        """TO folders (2 levels deep) should have a media/ directory."""
        for group_dir in CONTENT_DIR.iterdir():
            if not group_dir.is_dir():
                continue
            for to_dir in group_dir.iterdir():
                if not to_dir.is_dir():
                    continue
                media_dir = to_dir / "media"
                assert media_dir.exists(), (
                    f"TO folder '{to_dir.relative_to(CONTENT_DIR)}' "
                    f"is missing a media/ directory"
                )
