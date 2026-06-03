import yaml
import re
from pathlib import Path
import tempfile
import shutil
import os

WIKI_DIR = Path("wiki")
CATEGORIES = ["career", "stock market", "cooking", "system"]

def get_category(filename, content, tags):
    if filename in ["index.md", "log.md", "AI-Industry-Map-2026.md"]:
        return "system"
    if "company" in tags or filename.endswith("-PM.md") or "-Map" in filename:
        return "career"
    # Default to career for now as per vault contents
    return "career"

def migrate_file(filepath: Path):
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        # Handle files without frontmatter
        filename = filepath.name
        category = get_category(filename, "", [])
        frontmatter = {'category': category}
        body = content
    else:
        frontmatter_raw = match.group(1)
        body = match.group(2)
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
        except yaml.YAMLError:
            print(f"Error parsing YAML in {filepath}")
            return

        filename = filepath.name
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        
        category = frontmatter.get('category') or frontmatter.get('subject') or get_category(filename, content, tags)
        
        if category == "cooking and baking":
            category = "cooking"
            
        # Remove old keys if any
        frontmatter.pop('subject', None)
        
        # Ensure 'category' is the first key by re-inserting into a new dict
        new_frontmatter = {'category': category}
        for k, v in frontmatter.items():
            if k != 'category':
                new_frontmatter[k] = v
        frontmatter = new_frontmatter
        
    # Reconstruct YAML using yaml.dump with sort_keys=False to preserve order
    # allow_unicode=True prevents escaping non-ascii chars if any
    new_yaml = yaml.dump(frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False)
    new_content = f"---\n{new_yaml}---\n{body}"

    # Atomic write: write to temp file then move
    # Using filepath.parent to ensure it's on the same filesystem
    fd, temp_path = tempfile.mkstemp(dir=filepath.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(new_content)
        shutil.move(temp_path, filepath)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Failed to write {filepath}: {e}")

if __name__ == "__main__":
    if WIKI_DIR.exists():
        for file in WIKI_DIR.glob("*.md"):
            migrate_file(file)
