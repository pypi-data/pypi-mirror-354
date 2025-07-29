from setuptools import setup, find_packages

setup(
    name="mcp-open-client",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "nicegui",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "mcp-open-client=mcp_open_client.main:main",
        ],
    },
    python_requires=">=3.7",
    description="MCP Open Client - A NiceGUI-based chat application for Claude",
    author="alejoair",
    author_email="alejoair@example.com",  # Replace with actual email if different
    url="https://github.com/alejoair/mcp-open-client",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "mcp_open_client": [
            "assets/**/*",
            "settings/*.json",
        ],
    },
)