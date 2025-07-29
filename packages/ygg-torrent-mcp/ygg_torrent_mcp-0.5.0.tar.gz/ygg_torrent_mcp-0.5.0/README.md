# YggTorrent MCP Server & Wrapper

[![PyPI version](https://badge.fury.io/py/ygg-torrent-mcp.svg)](https://badge.fury.io/py/ygg-torrent-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository provides a Python wrapper for the YggTorrent website and an MCP (Model Context Protocol) server to interact with it programmatically. This allows for easy integration of YggTorrent functionalities into other applications or services.

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
  - [Via MCP Clients](#via-mcp-clients)
    - [Example for Windsurf](#example-for-windsurf)
- [Contributing](#contributing)
- [License](#license)

## Features

-   API wrapper for [YggAPI](https://yggapi.eu/), an unofficial API for YggTorrent
-   **Your Ygg passkey is injected locally into the torrent file/magnet link, ensuring it's not exposed externally**
-   MCP server interface for standardized communication
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

If you want to contribute to the project or run it from the source code, this project uses Poetry for dependency management.

#### 1. Clone the Repository
```bash
git clone https://github.com/philogicae/ygg-torrent-mcp.git
cd ygg-torrent-mcp
```

#### 2. Install Dependencies using Poetry

After cloning, navigate into the project directory:
```bash
cd ygg-torrent-mcp
```
If you don't have Poetry installed, you can typically install it with pip:
```bash
pip install poetry
```
Ensure Poetry's scripts directory is in your system's PATH. For other installation methods, see the [official Poetry installation guide](https://python-poetry.org/docs/#installation).

Once Poetry is available, install all main and development dependencies (like `pytest`):
```bash
poetry install --with dev
```
This command reads the `pyproject.toml` file, resolves dependencies, and installs them into the project's virtual environment (Poetry will create one if not already in an activated environment).

If you only want to install the main runtime dependencies:
```bash
poetry install
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

### Via MCP Clients

Once the MCP server is running, you can interact with it using any MCP-compatible client. The server will expose endpoints for:

-   `search_torrents`: Search for torrents.
-   `get_torrent_details`: Get details of a specific torrent.
-   `get_magnet_link`: Get the magnet link for a torrent.
-   `download_torrent_file`: Download the .torrent file for a torrent.
-   `get_torrent_categories`: Get the categories of torrents.

#### Example for Windsurf

```json
{
  "mcpServers": {
    ...
    "mcp-ygg-torrent": {
      "serverUrl": "http://127.0.0.1:8000/sse"
    }
    ...
  }
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue. If you plan to contribute, please ensure your code passes linting and tests (details to be added if a test suite is set up).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.