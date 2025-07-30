from setuptools import setup, find_packages

setup(
    name="szetop-mcp-dev",
    version="1.2.1",
    description="MCP server for image recognition using vision APIs (Anthropic, OpenAI, Cloudflare Workers AI)",
    author="Mario & Contributors",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "mcp>=1.2.0",
        "anthropic>=0.8.0",
        "openai>=1.6.0",
        "python-dotenv>=1.0.0",
        "Pillow>=10.0.0",
        "pytesseract>=0.3.13",
        "httpx>=0.27.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "szetop-mcp-dev=backend_gen_server.server:main",
        ],
    },
)
