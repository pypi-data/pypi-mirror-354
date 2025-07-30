from setuptools import setup, find_packages
import os

# Read README if it exists, otherwise use a simple description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Generate consistent, professional READMEs from YAML config"

setup(
    name="auto-research-readme",
    version="1.0.0",
    description="Generate consistent, professional READMEs from YAML config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abdullah Ridwan",
    author_email="abdullahridwan@gmail.com",
    url="https://github.com/Stratum-Research/auto-research-readme",
    packages=find_packages(),
    include_package_data=True,
    package_data={"auto_readme": ["templates/*.j2"]},
    install_requires=[
        "PyYAML>=6.0",
        "Jinja2>=3.0",
    ],
    entry_points={
        "console_scripts": [
            "auto-research-readme=auto_readme.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    keywords="readme documentation yaml config generator markdown",
)
