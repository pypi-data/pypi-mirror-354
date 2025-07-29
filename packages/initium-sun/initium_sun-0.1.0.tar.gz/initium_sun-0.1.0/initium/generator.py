import os
import shutil
import re
import subprocess
import requests
import json
from pathlib import Path

TEMPLATE_TYPES = ['plc', 'hmi', 'ros', 'bioreactor']

def generate_project(project_name, project_type, create_remote=False):
    # Validate inputs
    if not re.match(r'^[a-z0-9_-]+$', project_name):
        raise ValueError("Invalid project name! Use lowercase letters, numbers, hyphens, or underscores")
    
    if project_type not in TEMPLATE_TYPES:
        raise ValueError(f"Invalid project type. Must be one of: {TEMPLATE_TYPES}")
    
    # Get package directory
    package_dir = Path(__file__).parent
    template_dir = package_dir / 'templates' / project_type
    
    # Create output directory
    output_dir = Path.cwd() / f"generated_{project_name}"
    output_dir.mkdir(exist_ok=True)
    
    # Copy templates
    for item in template_dir.iterdir():
        dest = output_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    
    # Process template files
    process_template_files(output_dir, project_name)
    
    print(f"✅ Created project at {output_dir}")
    
    if create_remote:
        create_gitlab_project(project_name, output_dir)

def process_template_files(output_dir, project_name):
    # Rename CI template
    ci_template = output_dir / 'ci_template.yml'
    if ci_template.exists():
        ci_template.rename(output_dir / '.gitlab-ci.yml')
    
    # Process README template
    readme_tpl = output_dir / 'README.md.tpl'
    if readme_tpl.exists():
        with open(readme_tpl, 'r') as f:
            content = f.read().replace('$PROJECT_NAME', project_name)
        with open(output_dir / 'README.md', 'w') as f:
            f.write(content)
        readme_tpl.unlink()

def create_gitlab_project(project_name, output_dir):
    pat_token = input("Enter GitLab PAT: ")
    # TODO: Implement GitLab API calls and git commands
    print("GitLab project creation not implemented yet") 