from setuptools import setup, find_packages

# Read version from package
def get_version():
    version_file = "ai_chat_manager/__init__.py"
    with open(version_file, 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return "1.0.0"

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cybercore-ai-chat-manager",
    version=get_version(),
    author="TeamMalina",
    author_email="contact@teammalina.dev",
    description="A modular AI API/chat manager supporting multiple backends",
    long_description=long_description,
    long_description_content_type="text/markdown",    url="https://github.com/TeamMalina/CyberCore",
    license="MIT",
    project_urls={
        "Homepage": "https://github.com/TeamMalina/CyberCore",
        "Repository": "https://github.com/TeamMalina/CyberCore",
        "Documentation": "https://github.com/TeamMalina/CyberCore/wiki",
        "Bug Reports": "https://github.com/TeamMalina/CyberCore/issues",
        "Changelog": "https://github.com/TeamMalina/CyberCore/blob/main/CHANGELOG.md",
    },    packages=find_packages(),
    # Don't automatically include license file
    include_license_file=False,
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
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0,<4.0.0",
        "requests>=2.31.0,<3.0.0",
        "httpx>=0.24.0,<1.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "pydantic-settings>=2.0.0,<3.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
        "pyyaml>=6.0,<7.0",
        "cryptography>=41.0.0,<42.0.0",
        "click>=8.1.0,<9.0.0",
        "rich>=13.0.0,<14.0.0",
        "prompt-toolkit>=3.0.0,<4.0.0",
        "python-dateutil>=2.8.0,<3.0.0",
        "tiktoken>=0.5.0,<1.0.0",
        "tenacity>=8.0.0,<9.0.0",
        "typing-extensions>=4.5.0,<5.0.0",
    ],
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
        "all": [
            "torch>=2.0.0",
            "transformers>=4.25.0",
            "elevenlabs>=0.2.0",
            "openai>=1.0.0",
            "anthropic>=0.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-chat-manager=ai_chat_manager.cli.main:main",
            "acm=ai_chat_manager.cli.main:main",
            "chat-manager=ai_chat_manager.cli.main:main",
            "acm-wrapper=ai_chat_manager.cli.wrapper:main",
        ],
    },
    keywords="ai chat bot openai api machine-learning nlp chatbot assistant",
    include_package_data=True,
    package_data={
        "ai_chat_manager": ["py.typed"],
    },
)
