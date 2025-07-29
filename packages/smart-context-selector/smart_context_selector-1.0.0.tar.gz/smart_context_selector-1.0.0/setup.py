from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-context-selector",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligently selects and bundles documentation for optimal AI assistant context",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-context-selector",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for core functionality
    ],
    entry_points={
        "console_scripts": [
            "smart-context=smart_context_selector.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "smart_context_selector": ["configs/*.json"],
    },
    keywords="ai, documentation, context, claude, gpt, automation, n8n",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/smart-context-selector/issues",
        "Source": "https://github.com/yourusername/smart-context-selector",
    },
)