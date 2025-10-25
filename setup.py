from setuptools import setup, find_packages

setup(
    name="trackhs-mcp",
    version="2.0.0",
    description="Servidor MCP para Track HS API implementado con FastMCP",
    author="Track HS Team",
    author_email="team@trackhs.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "fastmcp>=0.4.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
