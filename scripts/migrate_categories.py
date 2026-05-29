import os
import yaml
import re

WIKI_DIR = "wiki"
CATEGORIES = ["career", "stock market", "cooking", "system"]

def get_category(filename, content, tags):
    if filename in ["index.md", "log.md", "AI-Industry-Map-2026.md"]:
        return "system"
    if "company" in tags or filename.endswith("-PM.md") or "-Map" in filename:
        return "career"
    # Default to career for now as per vault contents
    return "career"

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        # Handle files without frontmatter
        filename = os.path.basename(filepath)
        category = get_category(filename, "", [])
        new_content = f"---\ncategory: {category}\n---\n\n" + content
    else:
        frontmatter_raw = match.group(1)
        body = match.group(2)
        try:
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
        except yaml.YAMLError:
            print(f"Error parsing YAML in {filepath}")
            return

        filename = os.path.basename(filepath)
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        
        category = frontmatter.get('category') or frontmatter.get('subject') or get_category(filename, content, tags)
        
        if category == "cooking and baking":
            category = "cooking"
            
        # Remove old keys if any
        frontmatter.pop('subject', None)
        frontmatter['category'] = category
        
        # Reconstruct YAML with category first
        ordered_keys = ['category'] + [k for k in frontmatter.keys() if k != 'category']
        new_yaml = ""
        for k in ordered_keys:
            val = frontmatter[k]
            if isinstance(val, list):
                new_yaml += f"{k}: [{', '.join(val)}]\n"
            else:
                new_yaml += f"{k}: {val}\n"
        
        new_content = f"---\n{new_yaml}---\n{body}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    if os.path.exists(WIKI_DIR):
        for filename in os.listdir(WIKI_DIR):
            if filename.endswith(".md"):
                migrate_file(os.path.join(WIKI_DIR, filename))
