#!/usr/bin/env python
"""
Convert Lightwave configuration files to YAML format

This script converts JSON and custom format files to YAML according to the Lightwave YAML standard.
"""

import os
import json
import re
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

# Set to serialize None as null in YAML
def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', 'null')

yaml.add_representer(type(None), represent_none)

def snake_case(s: str) -> str:
    """Convert camelCase or kebab-case to snake_case"""
    s = re.sub(r'[-\s]', '_', s)
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()

def convert_dict_keys_to_snake_case(d: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively convert all dictionary keys to snake_case"""
    if not isinstance(d, dict):
        return d
    
    result = {}
    for key, value in d.items():
        new_key = snake_case(key)
        
        if isinstance(value, dict):
            result[new_key] = convert_dict_keys_to_snake_case(value)
        elif isinstance(value, list):
            result[new_key] = [
                convert_dict_keys_to_snake_case(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[new_key] = value
            
    return result

def convert_json_to_yaml(json_file: str, output_file: str, module: str = None) -> None:
    """Convert a JSON file to YAML format"""
    print(f"Converting {json_file} to YAML format...")
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Convert keys to snake_case
        data = convert_dict_keys_to_snake_case(data)
        
        # Add standard metadata
        if 'version' not in data:
            if 'version' in data:
                data['version'] = data.pop('version')
            else:
                data['version'] = "1.0.0"
                
        if 'updated' not in data:
            data['updated'] = datetime.now().strftime("%Y-%m-%d")
            
        if module and 'module' not in data:
            data['module'] = module
            
        # Extract filename without extension
        base_name = os.path.basename(json_file)
        file_name = os.path.splitext(base_name)[0]
        
        if 'description' not in data and 'description' not in data:
            data['description'] = f"Configuration for {file_name}"
        
        # Write YAML file
        with open(output_file, 'w') as f:
            f.write(f"# {data.get('description', 'Lightwave Configuration')}\n")
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        print(f"✅ Successfully converted to {output_file}")
    except Exception as e:
        print(f"❌ Error converting {json_file}: {str(e)}")

def parse_lightwave_rules(file_path: str) -> Dict[str, Any]:
    """Parse a .lightwaverules file into a structured dictionary"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split into sections
    section_pattern = r'---\s*([A-Z_]+)\s*---\s*description:\s*(.*?)\s*globs:\s*(.*?)\s*(?:filesToApplyRule:\s*(.*?)\s*)?(?:alwaysApply:\s*(.*?)\s*)?---\s*(.*?)(?=---\s*[A-Z_]+\s*---|$)'
    sections = re.findall(section_pattern, content, re.DOTALL)
    
    result = {
        "version": "1.0.0",
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "description": "Lightwave Rules Configuration",
        "sections": []
    }
    
    for section in sections:
        name, description, globs, files_to_apply, always_apply, content = section
        
        # Parse the content into structured format
        headings = re.split(r'\n\s*-\s*\*\*(.*?)\*\*\s*\n', content)
        parsed_content = []
        
        for i in range(1, len(headings), 2):
            heading = headings[i].strip()
            content_text = headings[i+1] if i+1 < len(headings) else ""
            
            # Extract bullet points
            items = []
            for line in content_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    items.append(line[2:])
            
            # Extract code blocks
            code_blocks = re.findall(r'```(.*?)```', content_text, re.DOTALL)
            code = code_blocks[0] if code_blocks else None
            
            heading_data = {
                "heading": heading,
                "items": items
            }
            
            if code:
                heading_data["code"] = code
                
            parsed_content.append(heading_data)
        
        section_data = {
            "name": name,
            "description": description.strip(),
            "globs": globs.strip(),
            "content": parsed_content
        }
        
        if files_to_apply and files_to_apply.strip():
            section_data["files_to_apply"] = files_to_apply.strip()
            
        if always_apply and always_apply.strip().lower() == 'true':
            section_data["always_apply"] = True
        
        result["sections"].append(section_data)
    
    return result

def convert_lightwave_rules_to_yaml(rules_file: str, output_file: str) -> None:
    """Convert a .lightwaverules file to YAML format"""
    print(f"Converting {rules_file} to YAML format...")
    
    try:
        data = parse_lightwave_rules(rules_file)
        
        # Write YAML file
        with open(output_file, 'w') as f:
            f.write(f"# Lightwave Rules Configuration\n")
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        print(f"✅ Successfully converted to {output_file}")
    except Exception as e:
        print(f"❌ Error converting {rules_file}: {str(e)}")

def convert_text_to_yaml(text_file: str, output_file: str, module: str = None) -> None:
    """Convert a text file to structured YAML as best as possible"""
    print(f"Converting {text_file} to YAML format...")
    
    try:
        with open(text_file, 'r') as f:
            content = f.read()
        
        # Extract the title and main sections
        lines = content.split('\n')
        title = lines[0].strip('# ')
        
        # Basic structure for the YAML
        data = {
            "version": "1.0.0",
            "updated": datetime.now().strftime("%Y-%m-%d"),
            "description": title,
        }
        
        if module:
            data["module"] = module
        
        # Parse sections (marked by ## in markdown)
        sections = []
        current_section = None
        current_content = []
        
        for line in lines[1:]:
            if line.startswith('## '):
                if current_section:
                    sections.append({
                        "name": current_section,
                        "content": '\n'.join(current_content)
                    })
                current_section = line.strip('# ')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section:
            sections.append({
                "name": current_section,
                "content": '\n'.join(current_content)
            })
        
        # Add sections to data
        if sections:
            data["sections"] = sections
            
        # Parse content for structured data where possible
        for section in data.get("sections", []):
            content = section.pop("content", "")
            parsed_items = []
            
            # Try to parse bullet points
            bullet_points = re.findall(r'^\s*-\s*(.*?)$', content, re.MULTILINE)
            if bullet_points:
                section["items"] = bullet_points
            else:
                # If no bullet points, just use the text as is
                section["text"] = content.strip()
        
        # Write YAML file
        with open(output_file, 'w') as f:
            f.write(f"# {title}\n")
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
        print(f"✅ Successfully converted to {output_file}")
    except Exception as e:
        print(f"❌ Error converting {text_file}: {str(e)}")

def process_directory(directory: str, dry_run: bool = False, module: str = None) -> None:
    """Process all files in a directory and convert them to YAML"""
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"❌ Directory {directory} does not exist")
        return
    
    for file_path in directory_path.glob('*'):
        if file_path.is_file():
            extension = file_path.suffix.lower()
            base_name = file_path.stem
            output_file = file_path.parent / f"{base_name}.yaml"
            
            # Skip if the output file already exists and has the same name
            if output_file == file_path:
                continue
                
            if extension == '.json':
                if dry_run:
                    print(f"Would convert {file_path} to {output_file}")
                else:
                    convert_json_to_yaml(str(file_path), str(output_file), module)
            elif file_path.name == '.lightwaverules' or extension == '.lightwaverules':
                if dry_run:
                    print(f"Would convert {file_path} to {output_file}")
                else:
                    convert_lightwave_rules_to_yaml(str(file_path), str(output_file))
            elif extension in ['.txt', '.md']:
                if dry_run:
                    print(f"Would convert {file_path} to {output_file}")
                else:
                    convert_text_to_yaml(str(file_path), str(output_file), module)

def main() -> None:
    parser = argparse.ArgumentParser(description='Convert Lightwave configuration files to YAML')
    parser.add_argument('--file', type=str, help='Path to a single file to convert')
    parser.add_argument('--directory', type=str, help='Path to a directory to process all files')
    parser.add_argument('--output', type=str, help='Output file path (when converting a single file)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be converted without actually converting')
    parser.add_argument('--module', type=str, help='Module name to add to the YAML metadata')
    
    args = parser.parse_args()
    
    if args.file:
        if not args.output and not args.dry_run:
            base_name = os.path.splitext(args.file)[0]
            args.output = f"{base_name}.yaml"
            
        file_extension = os.path.splitext(args.file)[1].lower()
        
        if args.dry_run:
            print(f"Would convert {args.file} to {args.output}")
        else:
            if file_extension == '.json':
                convert_json_to_yaml(args.file, args.output, args.module)
            elif args.file.endswith('.lightwaverules') or file_extension == '.lightwaverules':
                convert_lightwave_rules_to_yaml(args.file, args.output)
            elif file_extension in ['.txt', '.md']:
                convert_text_to_yaml(args.file, args.output, args.module)
            else:
                print(f"❌ Unsupported file type: {file_extension}")
    elif args.directory:
        process_directory(args.directory, args.dry_run, args.module)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 