# AIND Metadata access MCP server

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
![Interrogate](https://img.shields.io/badge/interrogate-94.4%25-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov)
![Python](https://img.shields.io/badge/python->=3.11-blue?logo=python)

## Setting up your desktop for installing MCP servers

1. Downloading UV to your desktop
( Unsure about the necessity of this step but it definitely helps having the package configured locally)

- on Mac Terminal

```bash
brew install uv

# Or, alternatively:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- on Windows Powershell

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Create virtual environment with python 3.11 in IDE

```bash
conda create -n <my_env> python=3.11
conda activate <my_env>
```

- Or, alternatively:

```bash
py -3.11 -m venv .venv

# Either Windows
.venv\Scripts\Activate.ps1 
# or Mac
source .venv/bin/activate 
```

3. Run the following commands in your IDE terminal. The `uvx` command should ideally take 3 minutes to start up without errors.

```bash
pip install uv
uvx aind-metadata-mcp
```

The `uvx` command should ideally take 3 minutes to start up without errors. If all goes well, and you see the following notice - `Starting MCP server 'aind_data_access' with transport 'stdio'`-, you should be good for the set up in your client of choice!

## Instructions for use in MCP clients

JSON Config files to add MCP servers in clients should be structured like this

```bash
{
    "mcpServers": {

    }
}
```

Insert the following lines into the mcpServers dictionary

```bash

"aind_data_access": {
    "command": "uvx",
    "args": ["aind-metadata-mcp"]
}

```

### Claude Desktop App

- Click the three lines at the top left of the screen.
- File > Settings > Developer > Edit config

### Cline in VSCode

- Ensure that Cline is downloaded to VScode
- Click the three stacked rectangles at the top right of the Cline window
- Installed > Configure MCP Servers
- Close and reopen VSCode

### Github Copilot in VSCode

- Command palette (ctr shift p)
- Search for MCP: Add server
- Select edit in settings.json
- Input `aind-data-access` dictionary under mcp > servers
- Close and reopen VSCode
- In Copilot chat -> Select agent mode -> Click the three stacked rectangles to configure tools
- In order to enable the agent to reply with context of the AIND API, you'll have to manually add the .txt files (under resources) in this repository
