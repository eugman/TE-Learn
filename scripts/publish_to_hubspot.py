"""
Publish EO content to HubSpot.

HubSpot options:
  - Blog Posts: Full API support (create, update, publish). Best option.
  - Site Pages: API exists but complex layoutSections payload. Overkill.
  - Knowledge Base: No API. Manual or browser automation only.

Blog Posts API is the recommended path:
  - POST /cms/v3/blogs/posts/ with postBody as HTML
  - Supports draft/publish workflow
  - Clean URLs for LMS linking

Usage:
    python scripts/publish_to_hubspot.py --eo <uid> --target blog
    python scripts/publish_to_hubspot.py --eo <uid> --target blog --dry-run
    python scripts/publish_to_hubspot.py --eo <uid> --target kb --interactive

Prerequisites:
    pip install requests pyyaml markdown playwright
    playwright install chromium  # only for KB target

Environment variables:
    HUBSPOT_ACCESS_TOKEN - HubSpot private app access token
    HUBSPOT_BLOG_ID      - Content group ID for the target blog
"""

import argparse
import os
import sys
from pathlib import Path


def find_eo_file(uid: str) -> Path | None:
    """Find the EO markdown file by uid."""
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
    """Render markdown to HTML."""
    import markdown

    return markdown.markdown(body, extensions=["tables", "fenced_code"])


def publish_blog_post(
    title: str, slug: str, html_content: str, *, publish: bool = False
) -> None:
    """Publish as a HubSpot blog post via CMS API.

    API: https://developers.hubspot.com/docs/api/cms/blog-posts
    Creates as DRAFT by default. Pass --publish to go live immediately.
    """
    import requests

    token = os.environ.get("HUBSPOT_ACCESS_TOKEN", "")
    if not token:
        print("Error: Set HUBSPOT_ACCESS_TOKEN environment variable")
        print("Create a private app at Settings → Integrations → Private Apps")
        print("Required scope: cms.knowledge_base.articles.write (or content)")
        sys.exit(1)

    blog_id = os.environ.get("HUBSPOT_BLOG_ID", "")

    payload: dict = {
        "name": title,
        "slug": slug,
        "postBody": html_content,
        "state": "PUBLISHED" if publish else "DRAFT",
    }
    if blog_id:
        payload["contentGroupId"] = blog_id

    resp = requests.post(
        "https://api.hubapi.com/cms/v3/blogs/posts",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if resp.status_code == 201:
        post = resp.json()
        print(f"Created {'published' if publish else 'draft'} blog post.")
        print(f"  ID: {post.get('id')}")
        print(f"  URL: {post.get('url', 'N/A')}")
    else:
        print(f"Error {resp.status_code}: {resp.text[:500]}")
        sys.exit(1)


def publish_kb_interactive(title: str, html_content: str) -> None:
    """Publish to HubSpot KB via browser automation (no API available).

    Knowledge Base requires Service Hub Professional or Enterprise.
    """
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://app.hubspot.com")
        print("1. Log in to HubSpot")
        print("2. Navigate to Service → Knowledge Base")
        print("3. Click 'Create article'")
        print("4. Click into the article body")
        print("5. Press Enter here to paste content...")
        input()

        # Paste HTML via clipboard API
        page.evaluate(
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

        print(f"Content for '{title}' pasted. Review and close browser when done.")
        page.wait_for_event("close", timeout=0)
        browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish EO content to HubSpot")
    parser.add_argument("--eo", required=True, help="EO uid")
    parser.add_argument(
        "--target",
        choices=["blog", "kb"],
        default="blog",
        help="HubSpot content type (default: blog)",
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately (blog only, default is draft)",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Manual login for KB"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    eo_file = find_eo_file(args.eo)
    if not eo_file:
        print(f"Error: No EO file found with uid '{args.eo}'")
        sys.exit(1)

    metadata, body = parse_frontmatter(eo_file)
    html = render_markdown(body)
    title = metadata.get("title", args.eo)
    slug = metadata.get("uid", args.eo)

    if args.dry_run:
        print(f"Target: HubSpot {args.target}")
        print(f"Title: {title}")
        print(f"Slug: {slug}")
        print(f"HTML length: {len(html)} chars")
        return

    if args.target == "blog":
        publish_blog_post(title, slug, html, publish=args.publish)
    else:
        publish_kb_interactive(title, html)


if __name__ == "__main__":
    main()
