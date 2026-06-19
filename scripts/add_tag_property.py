import os
import re
import yaml
from pathlib import Path

WIKI_DIR = Path("wiki")

def get_frontmatter(content):
    match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not match:
        return None, content
    raw_yaml = match.group(1)
    body = content[match.end():]
    try:
        data = yaml.safe_load(raw_yaml)
        return data, body
    except yaml.YAMLError:
        return None, content

def get_stage_and_tag(filepath: Path):
    parts = filepath.relative_to(WIKI_DIR).parts
    
    if len(parts) >= 2 and parts[0] == "research":
        return "research", parts[1]
    elif len(parts) >= 1 and parts[0] == "cooking":
        return "cooking", "cooking"
    elif len(parts) >= 1 and parts[0] == "projects":
        return "projects", "projects"
    elif len(parts) >= 1 and parts[0] == "ideation":
        return "ideation", "ideation"
    else:
        return "general", "system"

def process_file(filepath: Path):
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return
        
    data, body = get_frontmatter(content)
    if data is None:
        data = {}
        
    stage, tag = get_stage_and_tag(filepath)
    category = data.get("category", "system")
    
    # Reconstruct dictionary to enforce strict order
    new_data = {
        "stage": stage,
        "category": category,
        "tag": tag
    }
    
    # Add other keys sorted alphabetically
    other_keys = sorted([k for k in data.keys() if k not in ["stage", "category", "tag"]])
    for k in other_keys:
        new_data[k] = data[k]
        
    # Serialize back to frontmatter
    yaml_str = yaml.dump(new_data, sort_keys=False, allow_unicode=True, default_flow_style=False)
    new_content = f"---\n{yaml_str}---\n{body}"
    
    filepath.write_text(new_content, encoding="utf-8")
    print(f"Updated: {filepath}")

def main():
    if not WIKI_DIR.exists():
        print("wiki/ directory not found.")
        return
        
    for filepath in WIKI_DIR.rglob("*.md"):
        if "restaurants" in filepath.parts:
            continue
        process_file(filepath)

if __name__ == "__main__":
    main()
