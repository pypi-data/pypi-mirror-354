#!/usr/bin/env python3
"""
AI Chat Manager - Setup Configuration
A modular AI API/chat manager supporting multiple backends
"""

from setuptools import setup, find_packages
from pathlib import Path
import re

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read version from __init__.py
def get_version():
    init_file = this_directory / "ai_chat_manager" / "__init__.py"
    content = init_file.read_text(encoding='utf-8')
    match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string")

# Read requirements
def get_requirements():
    req_file = this_directory / "requirements.txt"
    if req_file.exists():
        return [
            line.strip() 
            for line in req_file.read_text(encoding='utf-8').splitlines()
            if line.strip() and not line.startswith("#")
        ]
    return []

setup(
    name="cybercore-ai-chat-manager",
    version=get_version(),
    author="TeamMalina",
    author_email="contact@teammalina.dev",
    description="A modular AI API/chat manager supporting multiple backends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TeamMalina/CyberCore",
    project_urls={
        "Bug Reports": "https://github.com/TeamMalina/CyberCore/issues",
        "Source": "https://github.com/TeamMalina/CyberCore",
        "Documentation": "https://github.com/TeamMalina/CyberCore/wiki",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
    ],
    keywords="ai, chat, bot, openai, api, machine-learning, nlp, chatbot, assistant",
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "all": [
            "torch>=2.0.0",
            "transformers>=4.25.0",
            "elevenlabs>=0.2.0",
            "openai>=1.0.0",
            "anthropic>=0.3.0",
            "cohere>=4.0.0",
        ],
        "audio": [
            "elevenlabs>=0.2.0",
            "pydub>=0.25.0",
            "soundfile>=0.12.0",
        ],
        "local": [
            "torch>=2.0.0",
            "transformers>=4.25.0",
            "accelerate>=0.20.0",
        ],
        "enterprise": [
            "redis>=4.5.0",
            "celery>=5.2.0",
            "prometheus_client>=0.16.0",
            "sentry-sdk>=1.20.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-chat-manager=ai_chat_manager.cli.main:main",
            "acm=ai_chat_manager.cli.main:main",
            "chat-manager=ai_chat_manager.cli.main:main",
        ],
    },
    package_data={
        "ai_chat_manager": [
            "templates/*.yaml",
            "templates/*.json",
            "static/*",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
)