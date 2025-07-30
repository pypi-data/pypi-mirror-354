# Auto Research README

[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
![Python](https://img.shields.io/badge/python-3.8+-blue)
[![PyPI](https://img.shields.io/badge/PyPI-1.0.0-green)](https://pypi.org)

Generate consistent, professional READMEs from YAML configuration files.

## Features

- 🚀 **Fast**: Generate complete READMEs in seconds
- 📝 **Consistent**: Maintain uniform documentation across all your projects  
- 🔧 **Configurable**: Everything controlled via simple YAML config
- 🏷️ **HuggingFace Ready**: Includes YAML frontmatter for HuggingFace datasets
- 📊 **Multi-format**: Generate READMEs, citations, metadata, and more
- 📦 **Easy to Use**: Simple CLI interface

## Installation

```bash
pip install auto-research-readme
```

## Quick Start

1. **Initialize a new project**:
   ```bash
   auto-research-readme init
   ```

2. **Edit your config**:
   ```bash
   # Edit config/config.yaml with your project details
   nano config/config.yaml
   ```

3. **Generate README and LICENSE**:
   ```bash
   auto-research-readme make readme
   ```

## Usage

### Commands

- `auto-research-readme init` - Initialize new project with sample config
- `auto-research-readme make readme` - Generate README.md and LICENSE from config
- `auto-research-readme make all` - Generate all repository files (README, LICENSE, citation.bib)

### Project Structure

After running `auto-research-readme init`, you'll have:

```
your-project/
├── config/
│   ├── config.yaml      # Your project configuration
│   └── assets/          # Logo, banner, etc.
│       ├── logo.png
│       └── banner.png
└── README.md            # Generated README
```

### Configuration

The `config.yaml` file controls everything:

```yaml
title: "My-Dataset"
version: "1.0"
published: "2025-01-01"
tagline: "A sample dataset for demonstration"
description: "This is a sample dataset description."
doi: "10.5281/zenodo.123456"

# Metadata for HuggingFace/README  
language:
  - "en"
tags:
  - "machine-learning"
  - "dataset"
size_categories:
  - "1K<n<10K"

# Links
github_link: "https://github.com/yourusername/your-repo"
huggingface_link: "https://huggingface.co/datasets/yourusername/your-dataset"
zenodo_link: "https://zenodo.org/record/123456"

# Author Info
maintainer: "your.email@example.com"
contributors:
  - name: "Your Name"
    orcid: "0000-0000-0000-0000"
    email: "your.email@example.com"
    affiliation: "Your Organization"
    role: "creator"
```

## Generated Output

The package generates essential repository files:

- **README.md** - Complete README with YAML frontmatter for HuggingFace
- **LICENSE** - MIT license  
- **citation.bib** - BibTeX citation

> **Note**: Both HuggingFace and Zenodo automatically pull metadata from your README and GitHub repository, so no additional JSON files are needed!

## For Contributors & Package Development

If you want to contribute to this package or modify it:

```bash
# Clone the repo
git clone https://github.com/Stratum-Research/auto-research-readme
cd auto-research-readme

# Set up development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Or use make commands
make dev-install
make test
make clean
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- **Author**: Abdullah Ridwan
- **Email**: abdullahridwan@gmail.com
- **Organization**: Stratum Research