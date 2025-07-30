#!/usr/bin/env python3
"""
Core README generation functionality.
"""

import json
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, PackageLoader


def load_config(config_path="config.yaml"):
    """Load YAML configuration file."""
    # Try config/config.yaml first, then config.yaml in current dir
    possible_paths = [
        Path("config") / "config.yaml",
        Path(config_path),
        Path("config.yaml"),
    ]

    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return yaml.safe_load(f)

    raise FileNotFoundError(
        "Could not find config.yaml in current directory or config/ folder"
    )


def generate_readme(config):
    """Generate README from template."""
    try:
        # Try to load from package templates first
        env = Environment(loader=PackageLoader("auto_readme", "templates"))
        template = env.get_template("readme.md.j2")
    except:
        # Fallback to local templates folder if package not installed
        env = Environment(loader=FileSystemLoader("templates/"))
        template = env.get_template("readme.md.j2")

    return template.render(**config)


def generate_huggingface_card(config):
    """Generate Hugging Face dataset card JSON."""
    return json.dumps(
        {
            "title": config["title"],
            "pretty_name": config["title"].lower(),
            "version": config["version"],
            "language": config.get("language", ["en"]),
            "license": "mit",
            "tags": config.get("tags", []),
            "description": config["description"],
            "authors": [
                {
                    "name": c["name"],
                    "email": c["email"],
                    "affiliation": c["affiliation"],
                    "orcid": c["orcid"],
                }
                for c in config.get("contributors", [])
            ],
        },
        indent=2,
    )


def generate_zenodo_metadata(config):
    """Generate Zenodo metadata JSON."""
    return json.dumps(
        {
            "upload_type": "dataset",
            "publication_date": config["published"],
            "title": config["title"],
            "creators": [
                {
                    "name": f"{c['name'].split()[-1]}, {' '.join(c['name'].split()[:-1])}",
                    "affiliation": c["affiliation"],
                    "orcid": c["orcid"],
                }
                for c in config.get("contributors", [])
            ],
            "description": config["description"],
            "license": "mit",
            "keywords": config.get("tags", []),
            "version": config["version"],
        },
        indent=2,
    )


def generate_citation(config):
    """Generate BibTeX citation."""
    return f"""@dataset{{{config["title"].lower().replace("-", "_").replace(" ", "_")}_data,
  title={{{config["title"]}: {config["tagline"]}}},
  author={{{" and ".join([c["name"] for c in config.get("contributors", [])])}}},
  year={{{config["published"][:4]}}},
  version={{{config["version"]}}},
  doi={{{config.get("doi", "")}}},
  url={{{config.get("huggingface_link", "")}}}
}}"""


def generate_license(config):
    """Generate MIT License."""
    year = config.get("published", "2025")[:4]
    author = config.get("contributors", [{}])[0].get("name", "Author")

    return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


def write_output(filename, content, output_dir="./"):
    """Write content to output file."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    (output_path / filename).write_text(content)
    print(f"✓ Generated: {filename}")
