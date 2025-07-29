from setuptools import setup, find_packages

setup(
    name="mcp-jira-tools",
    version="0.1.1",
    description="MCP server for Jira integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/yourusername/mcp-jira-tools",
    packages=find_packages(),
    install_requires=[
        "fastmcp",
        "jira",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "mcp-jira-tools-server = mcp_jira_tools.server:main"
        ]
    },
    python_requires=">=3.8",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 