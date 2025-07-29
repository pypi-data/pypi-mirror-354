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
    
    print(f"[+] Created project at {output_dir}")
    
    if create_remote:
        create_gitlab_project(project_name, output_dir)

def process_template_files(output_dir, project_name):
    # Rename CI template if it exists and target doesn't
    ci_template = output_dir / 'ci_template.yml'
    ci_target = output_dir / '.gitlab-ci.yml'
    if ci_template.exists() and not ci_target.exists():
        ci_template.rename(ci_target)
    
    # Process README template if it exists
    readme_tpl = output_dir / 'README.md.tpl'
    readme_target = output_dir / 'README.md'
    if readme_tpl.exists():
        if not readme_target.exists():
            with open(readme_tpl, 'r', encoding='utf-8') as f:
                content = f.read().replace('$PROJECT_NAME', project_name)
            with open(readme_target, 'w', encoding='utf-8') as f:
                f.write(content)
        readme_tpl.unlink(missing_ok=True)

def create_gitlab_project(project_name, output_dir):
    pat_token = input("Enter GitLab PAT: ")
    # TODO: Implement GitLab API calls and git commands
    print("GitLab project creation not implemented yet") 