# Browser Agent

A robust browser automation agent designed to interact with web pages programmatically, exposed via a FastAPI web interface. This project leverages Playwright for browser control and `mcp-agent` for core agent functionalities, providing a powerful and flexible solution for web scraping, automated testing, and other browser-based tasks.

## Features

*   **MCP Support:** MCP from playwright
*   **Asynchronous Operations:** Built with `asyncio` and `uvloop` for high performance and concurrency.
*   **Configurable:** Easily customize agent behavior through `mcp_agent.config.yaml`.
*   **Modular Design:** Integrates with `mcp-agent` for extensible agent capabilities.

## Installation

To set up the Browser Agent, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/priyank766/Browser_Agent_MCP.git
    cd browser-agent
    ```

2.  **Install `uv` (if you don't have it):**
    `uv` is a fast Python package installer and resolver.
    ```bash
    pip install uv
    ```

3.  **Install dependencies:**
    ```bash
    uv add -r requirements.txt
    ```

4.  **Check Node and NPM:**

    ```bash
    1. node --version
    2. npm --version
    ```

5. **Paste API Keys**

    Paste Google API Key in `mcp_agent.secrets.yaml`
    Choose Model IN `mcp_agents.config.yaml`

## Usage

To start the Browser Agent, run the following command:

```bash
streamlit run browser_agents.py
```

This will start the Web application, typically accessible at `http://127.0.0.1:8000`.

You can then change the agent provider from `mcp_agent.config.yaml`
Refer to the `browser_agent.py` file 

## Configuration

The agent's behavior can be configured using the `mcp_agent.config.yaml` file. This file allows you to set various parameters for the browser, agent behavior, and other settings.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
