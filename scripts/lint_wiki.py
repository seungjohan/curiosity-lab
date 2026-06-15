import os
import re

WIKI_DIR = "wiki"

def lint_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"File read error: {e}"]

    # 1. Check YAML frontmatter and category
    yaml_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not yaml_match:
        errors.append("Missing or malformed YAML frontmatter")
    else:
        yaml_content = yaml_match.group(1)
        if not re.search(r"^category:", yaml_content, re.MULTILINE):
            errors.append("Missing mandatory 'category' in YAML")

    # 2. Check Key Takeaway
    if "> [!IMPORTANT] Key Takeaway" not in content:
        errors.append("Missing '> [!IMPORTANT] Key Takeaway' block")

    # 3. Check Connections
    if "## 🔗 Connections" not in content:
        errors.append("Missing '## 🔗 Connections' section")

    return errors

def main():
    all_errors = {}
    for root, dirs, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                errors = lint_file(path)
                if errors:
                    all_errors[path] = errors

    if not all_errors:
        print("✅ All files pass linting!")
    else:
        print(f"Total files with errors: {len(all_errors)}")
        for path, errors in sorted(all_errors.items()):
            print(f"❌ {path}:")
            for error in errors:
                print(f"  - {error}")

if __name__ == "__main__":
    main()
