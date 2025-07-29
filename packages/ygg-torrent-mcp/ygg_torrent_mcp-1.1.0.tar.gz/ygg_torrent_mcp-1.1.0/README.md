# YggTorrent MCP Server & Wrapper

[![PyPI version](https://badge.fury.io/py/ygg-torrent-mcp.svg?kill_cache=1)](https://badge.fury.io/py/ygg-torrent-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/philogicae/ygg-torrent-mcp)

This repository provides a Python wrapper for the YggTorrent website and an MCP (Model Context Protocol) server to interact with it programmatically. This allows for easy integration of YggTorrent functionalities into other applications or services.

> [How to use it with MCP Clients](#via-mcp-clients)

## Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Option 1: Install from PyPI (Recommended for Users)](#option-1-install-from-pypi-recommended-for-users)
  - [Option 2: Local Development Setup](#option-2-local-development-setup)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create and Activate Virtual Environment](#2-create-and-activate-virtual-environment)
    - [3. Install Dependencies for Development](#3-install-dependencies-for-development)
    - [4. Configure Environment Variables](#4-configure-environment-variables)
    - [5. Run the MCP Server (Local Development)](#5-run-the-mcp-server-local-development)
  - [Option 3: Docker Setup](#option-3-docker-setup)
    - [1. Clone the Repository (if not already done)](#1-clone-the-repository-if-not-already-done)
    - [2. Configure Environment Variables (Docker)](#2-configure-environment-variables-docker)
    - [3. Build and Run with Docker Compose](#3-build-and-run-with-docker-compose)
    - [4. Accessing the Server (Docker)](#4-accessing-the-server-docker)
- [Usage](#usage)
  - [As Python Wrapper](#as-python-wrapper)
  - [As MCP Server](#as-mcp-server)
  - [As FastAPI Server](#as-fastapi-server)
  - [Via MCP Clients](#via-mcp-clients)
    - [Example with Windsurf](#example-with-windsurf)
- [Contributing](#contributing)
- [License](#license)

## Features

-   API wrapper for [YggAPI](https://yggapi.eu/), an unofficial API for YggTorrent
-   **Your Ygg passkey is injected locally into the torrent file/magnet link, ensuring it's not exposed externally**
-   MCP server interface for standardized communication (stdio, sse, streamable-http)
-   FastAPI server interface for alternative HTTP access (e.g., for direct API calls or testing)
-   Search for torrents on YggTorrent
-   Get details for a specific torrent
-   Retrieve magnet links
-   Retrieve torrent files
-   Retrieve torrent categories

## Setup

Choose one of the following methods to set up the project.

### Prerequisites

-   An active YggTorrent account with a passkey.
-   Python 3.10+ (required for PyPI install or local Python setup).
-   `pip` (Python package installer, usually comes with Python).
-   Docker and Docker Compose (required for Docker setup).

### Option 1: Install from PyPI (Recommended for Users)

If you just want to use the `ygg-torrent-mcp` package (either as a library or to run the MCP server), you can install it directly from PyPI:

```bash
pip install ygg-torrent-mcp
```

After installation, you'll need to configure environment variables:
1.  Create a `.env` file in the directory where you plan to run your script or the MCP server.
2.  Add your YggTorrent passkey to this file. You can find your passkey on YggTorrent by navigating to: `Mon compte` -> `Mes paramètres`. Your passkey is part of the tracker URL, like `http://tracker.p2p-world.net:8080/{YOUR_PASSKEY}/announce`.
```env
YGG_PASSKEY=your_passkey_here
```

To run the MCP server after PyPI installation:
```bash
python -m ygg_torrent
```

### Option 2: Local Development Setup

If you want to contribute to the project or run it from the source code, this project uses `uv` for fast Python packaging and virtual environment management.

#### 1. Clone the Repository
```bash
git clone https://github.com/philogicae/ygg-torrent-mcp.git
cd ygg-torrent-mcp
```

#### 2. Install Dependencies using `uv`

After cloning, navigate into the project directory:
```bash
cd ygg-torrent-mcp
```
This project uses [`uv`](https://github.com/astral-sh/uv), a fast Python package installer and resolver:
- Without python: [How to install uv](https://github.com/astral-sh/uv#installation)
- With python:
```bash
pip install uv
```

First, create a virtual environment using `uv`:
```bash
uv venv
```
Activate it:
```bash
# On Linux/macOS
source .venv/bin/activate
# On Windows (Command Prompt)
.venv\Scripts\activate.bat
# On Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
`uv` commands will typically auto-detect and use an active virtual environment or one named `.venv` in the project root.

Next, install the project and its dependencies from `pyproject.toml`:
```bash
uv pip install -e .
```

#### 3. Configure Environment Variables

Copy the `.env.example` file to `.env` in the root of the cloned repository:
```bash
cp .env.example .env
```
Then, edit the `.env` file and fill in your YggTorrent passkey. You can find your passkey on YggTorrent by navigating to: `Mon compte` -> `Mes paramètres`. Your passkey is part of the tracker URL, like `http://tracker.p2p-world.net:8080/{YOUR_PASSKEY}/announce`.
```env
YGG_PASSKEY=your_passkey_here
```

#### 4. Run the MCP Server (Local Development)
```bash
python -m ygg_torrent
```
The MCP server will be accessible locally on port 8000 by default.

### Option 3: Docker Setup

This project includes a `Dockerfile` and `docker-compose.yaml` for easy containerization.

#### 1. Clone the Repository (if not already done)
```bash
git clone https://github.com/philogicae/ygg-torrent-mcp.git
cd ygg-torrent-mcp
```
#### 2. Configure Environment Variables (Docker)

Copy the `.env.example` file to `.env` in the root of the cloned repository:
```bash
cp .env.example .env
```
Then, edit the `.env` file and fill in your YggTorrent passkey. You can find your passkey on YggTorrent by navigating to: `Mon compte` -> `Mes paramètres`. Your passkey is part of the tracker URL, like `http://tracker.p2p-world.net:8080/{YOUR_PASSKEY}/announce`.
```env
YGG_PASSKEY=your_passkey_here
```

#### 3. Build and Run with Docker Compose
```bash
docker-compose -f docker/compose.yaml up --build
```
This command will build the Docker image (if it doesn't exist yet) and start the MCP server service.

#### 4. Accessing the Server (Docker)

The MCP server, when run via Docker Compose using the provided `docker/compose.yaml`, will be accessible on port 8765 by default.

## Usage

### As Python Wrapper

```python
from ygg_torrent import ygg_api

results = ygg_api.search_torrents('...')
for torrent in results:
    print(f"{torrent.filename} | {torrent.size} | {torrent.seeders} SE | {torrent.leechers} LE | {torrent.downloads} DL | {torrent.date}")
```

### As MCP Server

```python
from ygg_torrent import ygg_mcp

ygg_mcp.run(transport="sse")
```

### As FastAPI Server

This project also includes a FastAPI server as an alternative way to interact with the YggTorrent functionalities via a standard HTTP API. This can be useful for direct API calls, integration with other web services, or for testing purposes.

**Running the FastAPI Server:**
```bash
# Dev
python -m ygg_torrent --fastapi
# Prod
uvicorn ygg_torrent.fastapi_server:app
```
- `--host <host>`: Default: `0.0.0.0`.
- `--port <port>`: Default: `8000`.
- `--reload`: Enables auto-reloading when code changes (useful for development).
- `--workers <workers>`: Default: `1`.

The FastAPI server will then be accessible at `http://<host>:<port>`

**Available Endpoints:**
The FastAPI server exposes similar functionalities to the MCP server. Key endpoints include:
- `/`: A simple health check endpoint. Returns `{"status": "ok"}`.
- `/docs`: Interactive API documentation (Swagger UI).
- `/redoc`: Alternative API documentation (ReDoc).

Environment variables (like `YGG_PASSKEY`) are configured the same way as for the MCP server (via an `.env` file in the project root).

### Via MCP Clients

Usable with any MCP-compatible client. Available tools:

-   `search_torrents`: Search for torrents.
-   `get_torrent_details`: Get details of a specific torrent.
-   `get_magnet_link`: Get the magnet link for a torrent.
-   `download_torrent_file`: Download the .torrent file for a torrent.

#### Example with Windsurf
Configuration:
```json
{
  "mcpServers": {
    ...
    # with stdio (only requires uv installed)
    "mcp-ygg-torrent": {
      "command": "uvx",
      "args": [
        "--from",
        "ygg-torrent-mcp",
        "--refresh",
        "ygg-torrent",
      ],
      "env": { "YGG_PASSKEY": "your_passkey_here" }
    }
    # with sse transport (requires installation)
    "mcp-ygg-torrent": {
      "serverUrl": "http://127.0.0.1:8000/sse"
    }
    # with streamable-http transport (requires installation)
    "mcp-ygg-torrent": {
      "serverUrl": "http://127.0.0.1:8000/mcp" # not yet supported by every client
    }
    ...
  }
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue. If you plan to contribute, please ensure your code passes linting and tests (details to be added if a test suite is set up).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.