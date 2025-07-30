from setuptools import setup, find_packages

setup(
    name="mcp-k8s-tools",
    version="0.1.3",
    description="MCP server for investigating Kubernetes clusters",
    author="Jonathan Kittell",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "pydantic",
        "python-dotenv",
        "kubernetes"
    ],
    entry_points={
        "console_scripts": [
            "mcp-k8s-tools-server = mcp_k8s_tools.server:main"
        ]
    },
) 