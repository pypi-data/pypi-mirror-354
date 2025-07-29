from pathlib import Path
import os
import shutil

THIS_DIR = Path(__file__).parent
INPUT_DIR = THIS_DIR / "input"
OUTPUT_DIR = THIS_DIR / "output"

def copy_templates() -> Path:
    """Copy the template files to output directory."""
    output_template_dir = OUTPUT_DIR / "obi-templates"
    os.makedirs(output_template_dir, exist_ok=True)
    for file in os.listdir(INPUT_DIR / "obi-templates"):
        # print(f"copying {file} to {output_template_dir / file}")
        shutil.copy(INPUT_DIR / "obi-templates" / file, output_template_dir / file)
    return output_template_dir