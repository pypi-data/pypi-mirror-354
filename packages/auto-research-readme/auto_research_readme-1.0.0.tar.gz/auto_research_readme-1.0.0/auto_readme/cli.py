#!/usr/bin/env python3
"""
Command-line interface for auto-readme-generator.
"""

import argparse
import sys
from pathlib import Path

from .generator import (
    load_config,
    generate_readme,
    generate_citation,
    generate_license,
    write_output,
)


def cmd_make_readme(args):
    """Generate README.md and LICENSE in the top level directory."""
    try:
        config = load_config(args.config)

        # generate README.md in current directory
        readme_content = generate_readme(config)
        write_output("README.md", readme_content)

        # generate LICENSE in current directory
        license_content = generate_license(config)
        write_output("LICENSE", license_content)

        print("✓ Generated README.md")
        print("✓ Generated LICENSE")
        print("🎉 Repository files generated successfully!")
    except Exception as e:
        print(f"❌ Error generating files: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_make_all(args):
    """Generate all repository files from config."""
    try:
        config = load_config(args.config)

        generators = {
            "README.md": generate_readme,
            "LICENSE": generate_license,
            "citation.bib": generate_citation,
        }

        for filename, generator in generators.items():
            try:
                content = generator(config)
                write_output(filename, content)
            except Exception as e:
                print(f"❌ Error generating {filename}: {e}", file=sys.stderr)

        print("✓ Generated README.md")
        print("✓ Generated LICENSE")
        print("✓ Generated citation.bib")
        print("🎉 All repository files generated successfully!")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_init(args):
    """Initialize a new project with sample config."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    assets_dir = config_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    sample_config = """title: "My-Dataset"
version: "1.0"
published: "2025-01-01"
tagline: "A sample dataset for demonstration"
description: "This is a sample dataset description. Replace with your actual description."
doi: "10.5281/zenodo.123456"

# metadata for HuggingFace/README  
language:
  - "en"
tags:
  - "machine-learning"
  - "dataset"
  - "sample"
size_categories:
  - "1K<n<10K"

logo_path: "config/assets/logo.png"
banner_path: "config/assets/banner.png"

# links
github_link: "https://github.com/yourusername/your-repo"
huggingface_link: "https://huggingface.co/datasets/yourusername/your-dataset"
zenodo_link: "https://zenodo.org/record/123456"

# author info
maintainer: "your.email@example.com"
contributors:
  - name: "Your Name"
    orcid: "0000-0000-0000-0000"
    email: "your.email@example.com"
    affiliation: "Your Organization"
    role: "creator"
"""

    config_file = config_dir / "config.yaml"
    if config_file.exists():
        print("⚠️  config/config.yaml already exists. Skipping...")
    else:
        config_file.write_text(sample_config)
        print("✓ Created config/config.yaml")

    # create placeholder asset files
    readme_assets = """# Assets Folder

Place your project assets here:
- `logo.png` - Your project logo (recommended: 150px height)
- `banner.png` - Banner image for README (recommended: 800px width)

These will be referenced in your README.md automatically.
"""

    (assets_dir / "README.md").write_text(readme_assets)
    print("✓ Created config/assets/ folder")
    print("\n🎉 Project initialized! Next steps:")
    print("1. Edit config/config.yaml with your project details")
    print("2. Add logo.png and banner.png to config/assets/")
    print("3. Run 'auto-research-readme make readme' to generate README.md and LICENSE")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate consistent, professional READMEs from YAML config",
        prog="auto-research-readme",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # make subcommand
    make_parser = subparsers.add_parser("make", help="Generate files from config")
    make_subparsers = make_parser.add_subparsers(
        dest="make_what", help="What to generate"
    )

    # make readme
    readme_parser = make_subparsers.add_parser(
        "readme", help="Generate README.md and LICENSE"
    )
    readme_parser.add_argument(
        "--config", default="config.yaml", help="Config file path"
    )
    readme_parser.set_defaults(func=cmd_make_readme)

    # make all
    all_parser = make_subparsers.add_parser("all", help="Generate all repository files")
    all_parser.add_argument("--config", default="config.yaml", help="Config file path")
    all_parser.set_defaults(func=cmd_make_all)

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize new project with sample config"
    )
    init_parser.set_defaults(func=cmd_init)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
