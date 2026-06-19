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

def test_restaurants_deleted():
    """Verify that the restaurants folder and its markdown files are deleted."""
    rest_dir = WIKI_DIR / "research" / "cooking" / "restaurants"
    assert not rest_dir.exists(), "wiki/research/cooking/restaurants directory should be deleted"

def test_frontmatter_rules():
    """Verify all wiki files follow frontmatter constraints: stage first, category second, tag third."""
    assert WIKI_DIR.exists(), "wiki directory must exist"
    
    # Exclude system/temporary directories or paths
    md_files = [p for p in WIKI_DIR.rglob("*.md") if "restaurants" not in p.parts]
    
    for filepath in md_files:
        content = filepath.read_text(encoding="utf-8")
        data, _ = get_frontmatter(content)
        
        # Files must have frontmatter
        assert data is not None, f"File {filepath} must contain valid YAML frontmatter"
        
        # Verify order of properties
        keys = list(data.keys())
        assert len(keys) >= 3, f"File {filepath} must have at least stage, category, and tag properties"
        assert keys[0] == "stage", f"File {filepath}: first key must be 'stage', got '{keys[0]}'"
        assert keys[1] == "category", f"File {filepath}: second key must be 'category', got '{keys[1]}'"
        assert keys[2] == "tag", f"File {filepath}: third key must be 'tag', got '{keys[2]}'"
        
        # Verify tag matches folder/category name rules
        expected_tag = None
        parts = filepath.relative_to(WIKI_DIR).parts
        
        if len(parts) >= 2 and parts[0] == "research":
            # wiki/research/{subfolder}/...
            expected_tag = parts[1]
        elif len(parts) >= 1 and parts[0] == "cooking":
            # wiki/cooking/...
            expected_tag = "cooking"
        elif len(parts) >= 1 and parts[0] == "projects":
            # wiki/projects/...
            expected_tag = "projects"
        elif len(parts) >= 1 and parts[0] == "ideation":
            # wiki/ideation/...
            expected_tag = "ideation"
        else:
            # Root wiki files
            expected_tag = "system"
            
        assert data["tag"] == expected_tag, f"File {filepath}: expected tag '{expected_tag}', got '{data['tag']}'"

def test_design_md_exists():
    """Verify root-level DESIGN.md exists and contains expected sections."""
    design_file = Path("DESIGN.md")
    assert design_file.exists(), "Root-level DESIGN.md must exist"
    
    content = design_file.read_text(encoding="utf-8")
    assert "# Knowledge OS: Design & Linking Standards" in content, "DESIGN.md must have standard title header"
    assert "Horizontal (Intra-Stage) Connections: MOC Hubs" in content, "DESIGN.md must document MOC Hubs"
    assert "Vertical (Cross-Stage) Connections: Hybrid Pipeline" in content, "DESIGN.md must document hybrid workflow connections"
    assert "Relative Paths" in content, "DESIGN.md must document relative paths"
    assert "Annotated Links" in content, "DESIGN.md must document annotated links"
