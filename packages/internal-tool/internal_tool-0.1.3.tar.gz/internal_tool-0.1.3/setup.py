# setup.py

import setuptools
from pathlib import Path

# read long description from README.md
this_dir = Path(__file__).parent
long_description = '' # (this_dir / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="internal-tool",                      # how users will install it
    version="0.1.3",
    author="yashaswini",
    author_email="goyashu@gmail.com",
    description="A Python agent for discovering and processing documents from Google Drive and Notion.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yashaswini2027/internal-tool",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pydantic",
        "python-dotenv",
        "google-api-python-client",
        "notion-client",
        "pandas",
        "openpyxl",
        "google-api-python-client",
        "google-auth",
        "python-docx",
        "PyPDF2",
        "sentence-transformers",
        "spacy",
        "requests",
        "numpy",
        "pydantic-settings",
        "tiktoken",
        "transformers",
        "torch"
    ],
    entry_points={
        "console_scripts": [
            "pr-agent-discover=pr_agent.scripts.discover_sources:main",
            "pr-agent-process=pr_agent.scripts.process_pending:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
