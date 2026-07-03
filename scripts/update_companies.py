import os
import re

directory = "/Users/seungjohan/Obsidian/researcher/wiki/"
files_to_process = [
    "Bear-Robotics.md", "Twelve-Labs.md", "Upstage.md", "MakinaRocks.md", 
    "AIMMO.md", "AItrics.md", "Allganize.md", "Coredotbio.md", 
    "DeepBrain-AI.md", "DeepX.md", "FriendliAI.md", "FuriosaAI.md", 
    "LINER.md", "Lunit.md", "MarqVision.md", "MediWhale.md", 
    "Mobilint.md", "Moloco.md", "Nota-AI.md", "Persona-AI.md", 
    "Rebellions.md", "Riiid.md", "Scatter-Lab.md", "Sendbird.md", 
    "Speak.md", "SqueezeBits.md", "Standigm.md", "Superb-AI.md", 
    "VoyagerX.md", "VUNO.md", "Wrtn-Technologies.md"
]

def update_file(filename):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"File {filename} not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle MakinaRocks specifically if it has no YAML
    if filename == "MakinaRocks.md" and not content.startswith("---"):
        new_yaml = "---\nindustry: [Industrial AI, Manufacturing, Enterprise Software]\nscale: Series B Scale-up\nhq: Seoul\ncountry: South Korea\ntags: [company, IndustrialAI, Manufacturing, MLOps]\nabout: Industrial AI startup specializing in anomaly detection and process optimization.\n---\n"
        new_content = new_yaml + content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return

    # Regex to find YAML block
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not yaml_match:
        print(f"No YAML found in {filename}")
        return

    yaml_content = yaml_match.group(1)
    lines = yaml_content.split('\n')
    new_lines = []
    hq_found = False
    tags_line_idx = -1
    
    hq_val = ""
    country_val = ""

    for i, line in enumerate(lines):
        if line.startswith('hq:'):
            hq_found = True
            hq_val = line[3:].strip()
            
            # Logic to split hq and country
            if hq_val.endswith(", South Korea"):
                country_val = "South Korea"
                hq_val = hq_val.replace(", South Korea", "").strip()
            elif hq_val.endswith(", USA"):
                country_val = "USA"
                hq_val = hq_val.replace(", USA", "").strip()
            elif hq_val.endswith(", CA"):
                country_val = "USA"
                # Keep CA in hq as it is City, State
            elif hq_val.endswith(", Japan"):
                country_val = "Japan"
                hq_val = hq_val.replace(", Japan", "").strip()
            elif hq_val == "Seoul": # Edge case for already updated or partially missing
                country_val = "South Korea"
            
            new_lines.append(f"hq: {hq_val}")
            if country_val:
                new_lines.append(f"country: {country_val}")
        elif line.startswith('tags:'):
            tags_line_idx = len(new_lines)
            if "company" not in line:
                if line.strip().endswith(']'):
                    new_line = line.replace(']', ', company]')
                else:
                    new_line = line + ", company"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if hq_found:
        new_yaml = "---\n" + "\n".join(new_lines) + "\n---"
        new_content = content.replace(yaml_match.group(0), new_yaml + "\n")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No hq found in {filename}")

for filename in files_to_process:
    update_file(filename)
