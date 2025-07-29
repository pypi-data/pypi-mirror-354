#!/usr/bin/env python
"""Inject a folder structure into the README.md file."""

import re
import json
import time
from pathlib import Path

import requests

# Custom markers for start and end
_START_MARKER = "<!-- dir-tree-start -->"
_END_MARKER = "<!-- dir-tree-end -->"

# Customize excluded folders or files here
_EXCLUDED_DIRS = {
    ".git",
    ".env",
    "env",
    "venv",
    ".venv",
    ".idea",
    ".run",
    ".ruff_cache",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".DS_Store",
    "dist",
    "docs",
    "logs",
    "inject_tree.py",
}


def _get_icon(path: Path | str, _fa: str = "solid") -> str:
    """Returns a corresponding icon representation for a given file or directory path."""
    path = Path(path) if isinstance(path, str) else path
    fa = "-" if _fa.strip().lower() in ["fa", "regular"] else ""
    ext = path.suffix.lower()

    if path.is_dir():
        return "📁"
    if path.name.lower() == ".gitignore":
        return "🚫"
    if ext == ".py":
        ext = ".python"

    now = time.time()
    ext_icon_map = {}
    base_url = "https://bitbytelab.github.io/assets/"
    ext_icon_map_path = Path("file_ext_icon_map.json")
    if not ext_icon_map_path.exists() or now - ext_icon_map_path.stat().st_mtime > 86400:  # noqa: PLR2004
        try:
            ext_icon_map = requests.get(
                f"{base_url}file-ext/file_ext_icon_map.json", timeout=30
            ).json()
            ext_icon_map_path.write_text(json.dumps(ext_icon_map, indent=2), encoding="utf-8")
        except (Exception,) as e:
            print(f"Failed to fetch file_ext_icon_map.json: {e}")
    else:
        print("Using cached file_ext_icon_map.json")
        ext_icon_map = json.loads(ext_icon_map_path.read_text(encoding="utf-8"))

    w, h = 12, 14

    if ext_icon_map:
        ext_icon_map["png"] = set(ext_icon_map["png"])
        ext_icon_map["svg"] = set(ext_icon_map["svg"])
        if ext in ext_icon_map.get("svg", {}):
            print(f"hitting svg: {ext}")

            return f'<img src="{base_url}file-ext/svg/{ext[1:]}.svg" alt="{ext}" width="{w}">'

    fa_url = f"{base_url}fa/svg/"
    ext_fa_svg_map = {
        ".py": f"{fa_url}python{fa}.svg",
        ".txt": f"{fa_url}text-lines{fa}.svg",
        ".xls": f"{fa_url}file-excel{fa}.svg",
        ".xlsx": f"{fa_url}file-excel{fa}.svg",
        # ".csv": f"{fa_url}file-csv{fa}.svg",
        # ".pdf": f"{fa_url}file-pdf{fa}.svg",
        ".rar": f"{fa_url}file-zipper{fa}.svg",
        ".tar": f"{fa_url}file-zipper{fa}.svg",
        ".gz": f"{fa_url}file-zipper{fa}.svg",
        ".7z": f"{fa_url}file-zipper{fa}.svg",
        ".doc": f"{fa_url}file-word{fa}.svg",
        ".docx": f"{fa_url}file-word{fa}.svg",
        ".ppt": f"{fa_url}file-powerpoint{fa}.svg",
        ".pptx": f"{fa_url}file-powerpoint{fa}.svg",
        ".mov": f"{fa_url}file-video{fa}.svg",
        ".avi": f"{fa_url}file-video{fa}.svg",
        ".mp4": f"{fa_url}file-video{fa}.svg",
        ".mkv": f"{fa_url}file-video{fa}.svg",
        ".3gp": f"{fa_url}file-video{fa}.svg",
        ".webm": f"{fa_url}file-video{fa}.svg",
        ".css": f"{fa_url}css{fa}.svg",
        ".scss": f"{fa_url}css{fa}.svg",
        ".js": f"{fa_url}js{fa}.svg",
        ".ts": f"{fa_url}js{fa}.svg",
        ".tsv": f"{fa_url}table-list{fa}.svg",
        ".htm": f"{fa_url}code{fa}.svg",
        ".html": f"{fa_url}html5{fa}.svg",
        ".png": f"{fa_url}file-image{fa}.svg",
        ".jpg": f"{fa_url}file-image{fa}.svg",
        ".jpeg": f"{fa_url}file-image{fa}.svg",
        ".svg": f"{fa_url}file-image{fa}.svg",
        ".gif": f"{fa_url}file-image{fa}.svg",
        ".webp": f"{fa_url}file-image{fa}.svg",
    }

    if ext in ext_fa_svg_map:
        print(f"hitting fa svg: {ext}")
        return f'<img src="{ext_fa_svg_map[ext]}" alt="{ext}" width="{w}" color="white" />'

    if ext in ext_icon_map.get("png", {}):
        print(f"hitting png: {ext}")
        return f'<img src="{base_url}file-ext/32px/{ext[1:]}.png" alt="{ext}" width="{w}" >'

    ext_emoji_map = {
        ".md": "📝",
        ".toml": "⚙️",
        ".ini": "⚙️",
        ".env": "⚙️",
    }
    print(f"hitting last return: {ext}")
    return ext_emoji_map.get(ext, "📃")


def generate_tree(root_dir, prefix=""):
    """Recursively generate a folder structure tree."""
    entries = [
        e
        for e in sorted(root_dir.iterdir(), key=lambda p: p.name.lower())
        if ((e.name not in _EXCLUDED_DIRS and not e.name.startswith(".")) or e.name == ".gitignore")
    ]
    # Sort: directories first
    entries = [e for e in entries if e.is_dir()] + [e for e in entries if not e.is_dir()]

    tree_lines = []
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        # icon = "📁" if entry.is_dir() else "📄"
        icon = _get_icon(entry)
        tree_lines.append(f"{prefix}{connector}{icon} {entry.name}")

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            tree_lines.extend(generate_tree(entry, prefix + extension))

    return tree_lines


def update_readme_with_tree(readme_path, tree_lines):
    """Update the README.md file with the folder structure tree."""
    tree_md = "\n<pre>\n" + "\n".join(tree_lines) + "\n</pre>\n"
    content = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    folder_section_pattern = re.compile(
        rf"({re.escape(_START_MARKER)}\n)(.*?)(\n{re.escape(_END_MARKER)})", re.DOTALL
    )

    if _START_MARKER in content and _END_MARKER in content:
        # Replace the content between the markers
        content = re.sub(
            folder_section_pattern, lambda m: f"{m.group(1)}" + tree_md + f"{m.group(3)}", content
        )
    else:
        # Append the tree if no markers are found
        content += f"\n{_START_MARKER}" + tree_md + f"{_END_MARKER}\n"

    readme_path.write_text(content, encoding="utf-8")

    print("Folder Structure injected into README.md")


if __name__ == "__main__":
    project_root = Path()
    tree = generate_tree(project_root)
    print("\n".join(tree))

    readme_file = Path("README.md")
    update_readme_with_tree(readme_file, tree)
