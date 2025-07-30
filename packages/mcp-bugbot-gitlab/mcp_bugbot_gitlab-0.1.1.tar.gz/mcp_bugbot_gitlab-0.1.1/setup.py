from setuptools import setup, find_packages

setup(
    name="mcp-bugbot-gitlab",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "pydantic",
        "python-gitlab",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "mcp-bugbot-gitlab=mcp_bugbot_gitlab.server:main",
        ],
    },
    author="Jonathan Kittell",
    description="MCP server for GitLab merge request management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kitlabcode/mcp-bugbot-gitlab",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 