"""
Publish a single EO's markdown content to EasyGenerator via browser automation.

EasyGenerator uses a block-based editor (Course → Section → Page → Blocks).
Content blocks include: Text, Image, Media, Docs, Interactive, Embed/HTML.
Text blocks use a contenteditable rich text editor.
There is also an HTML content block with a code view toggle.

Strategy:
  1. Log in (interactive or env vars)
  2. Navigate to the target course/section/page
  3. Add a text block (or HTML block)
  4. Paste rendered HTML into the block via clipboard API

Selectors will need to be discovered via `npx playwright codegen app.easygenerator.com`
since EasyGenerator has no public DOM documentation. Look for:
  - contenteditable="true" divs (text blocks)
  - Editor library class names: ql-editor (Quill), ck-editor (CKEditor),
    ProseMirror, mce-content-body (TinyMCE)

Usage:
    python scripts/publish_to_easygenerator.py --eo <uid> --interactive
    python scripts/publish_to_easygenerator.py --eo <uid> --dry-run
    python scripts/publish_to_easygenerator.py --discover

Prerequisites:
    pip install playwright markdown pyyaml
    playwright install chromium

Environment variables:
    EG_EMAIL    - EasyGenerator login email
    EG_PASSWORD - EasyGenerator login password (or use --interactive)
"""

import argparse
import os
import sys
from pathlib import Path


def find_eo_file(uid: str) -> Path | None:
    """Find the EO markdown file by uid (filename without .md)."""
    content_dir = Path(__file__).parent.parent / "content"
    for md_file in content_dir.rglob("*.md"):
        if md_file.stem == uid:
            return md_file
    return None


def parse_frontmatter(file_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from a markdown file."""
    import yaml

    text = file_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text

    _, fm_text, body = text.split("---", 2)
    metadata = yaml.safe_load(fm_text)
    return metadata, body.strip()


def render_markdown(body: str) -> str:
    """Render markdown body to HTML for pasting into rich text editor."""
    import markdown

    return markdown.markdown(body, extensions=["tables", "fenced_code"])


def paste_html_into_editor(page: object, html_content: str) -> None:
    """Paste HTML into the focused contenteditable element via clipboard API.

    This works with most rich text editors (Quill, CKEditor, ProseMirror, TinyMCE).
    The target element must be focused before calling this.
    """
    page.evaluate(  # type: ignore[union-attr]
        """(html) => {
            const clipboardData = new DataTransfer();
            clipboardData.setData('text/html', html);
            const pasteEvent = new ClipboardEvent('paste', {
                clipboardData: clipboardData,
                bubbles: true,
                cancelable: true
            });
            document.activeElement.dispatchEvent(pasteEvent);
        }""",
        html_content,
    )


def discover_editor(page: object) -> None:
    """Inspect the page to identify the editor library and selectors."""
    info = page.evaluate(  # type: ignore[union-attr]
        """() => {
            const results = {};

            // Check for known editor libraries
            results.quill = !!document.querySelector('.ql-editor');
            results.ckeditor = !!document.querySelector('.ck-editor');
            results.prosemirror = !!document.querySelector('.ProseMirror');
            results.tinymce = !!document.querySelector('.mce-content-body');

            // Find contenteditable elements
            const editables = document.querySelectorAll('[contenteditable="true"]');
            results.contenteditable_count = editables.length;
            results.contenteditable_selectors = Array.from(editables).slice(0, 5).map(el => {
                return {
                    tag: el.tagName,
                    id: el.id,
                    classes: el.className,
                    role: el.getAttribute('role')
                };
            });

            // Find textareas (for HTML code view)
            const textareas = document.querySelectorAll('textarea');
            results.textarea_count = textareas.length;

            return results;
        }"""
    )
    print("Editor discovery results:")
    for key, value in info.items():
        print(f"  {key}: {value}")


def publish_to_easygenerator(
    uid: str,
    html_content: str,
    metadata: dict,
    *,
    interactive: bool = False,
    discover: bool = False,
) -> None:
    """Open EasyGenerator and assist with pasting content."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://app.easygenerator.com")

        if interactive:
            print("Log in manually in the browser.")
            print("Navigate to the target course → section → page.")
            print("Click into a text block (or add one).")
            print("Press Enter here when ready to paste content...")
            input()
        else:
            email = os.environ.get("EG_EMAIL", "")
            password = os.environ.get("EG_PASSWORD", "")
            if not email or not password:
                print("Set EG_EMAIL and EG_PASSWORD, or use --interactive")
                browser.close()
                sys.exit(1)
            # TODO: Fill in login selectors after discovery
            # page.fill('input[type="email"]', email)
            # page.fill('input[type="password"]', password)
            # page.click('button[type="submit"]')
            # page.wait_for_load_state("networkidle")
            print("Auto-login not yet implemented. Use --interactive for now.")
            print("Press Enter after logging in manually...")
            input()

        if discover:
            discover_editor(page)
            print("\nPress Enter to close browser...")
            input()
            browser.close()
            return

        # Paste content
        title = metadata.get("title", uid)
        print(f"Pasting content for: {title}")
        paste_html_into_editor(page, html_content)
        print("Content pasted. Review in browser, then close the window.")

        page.wait_for_event("close", timeout=0)
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish EO content to EasyGenerator")
    parser.add_argument("--eo", help="EO uid (filename without .md)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Render HTML but don't open browser"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Pause for manual login and navigation",
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Open EG and inspect editor DOM to find selectors",
    )
    args = parser.parse_args()

    if args.discover:
        publish_to_easygenerator("", "", {}, interactive=True, discover=True)
        return

    if not args.eo:
        parser.error("--eo is required unless using --discover")

    eo_file = find_eo_file(args.eo)
    if not eo_file:
        print(f"Error: No EO file found with uid '{args.eo}'")
        sys.exit(1)

    metadata, body = parse_frontmatter(eo_file)
    html = render_markdown(body)

    if args.dry_run:
        print(f"Title: {metadata.get('title', args.eo)}")
        print(f"Status: {metadata.get('status', 'unknown')}")
        print(f"File: {eo_file}")
        print(f"\n--- Rendered HTML ({len(html)} chars) ---\n")
        print(html[:500])
        if len(html) > 500:
            print(f"\n... ({len(html) - 500} more chars)")
        return

    publish_to_easygenerator(
        args.eo, html, metadata, interactive=args.interactive
    )


if __name__ == "__main__":
    main()
