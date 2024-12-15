# Setup Instructions

This guide provides detailed setup instructions for both Windows (PowerShell) and Linux/macOS (Bash) environments using the `uv` package installer.

## Installing `uv`

### Windows (PowerShell)

1. Open PowerShell as Administrator and run:

    ```powershell
    curl -LsSf https://astral.sh/uv/install.ps1 | powershell -c -
    ```

2. Close and reopen PowerShell to ensure `uv` is in your PATH

### Linux/macOS (Bash)

1. Open terminal and run:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. Close and reopen your terminal to ensure `uv` is in your PATH

## Project Setup

### Prerequisites

Ensure you have Git installed on your system:

- Windows: Download and install from [git-scm.com](https://git-scm.com/download/win)
- Linux: `sudo apt-get install git` (Ubuntu/Debian) or `sudo yum install git` (RHEL/CentOS)
- macOS: `brew install git` (using Homebrew)

### Windows (PowerShell) Setup

1. Create and activate virtual environment:

    ```powershell
    uv venv
    .venv/Scripts/activate
    ```

2. Install dependencies:

    ```powershell
    uv pip install -r requirements.txt
    ```

3. Create `.env` file:

    ```powershell
    New-Item .env
    ```

4. Add your environment variables to `.env`:

    ```ini
    NOTION_API_KEY=your_notion_api_key
    OPENAI_API_KEY_=your_openai_api_key
    NOTION_ENDPOINT=https://api.notion.com/v1
    NOTION_PAGE_ID=your_notion_page_id
    ```

### Linux/macOS (Bash) Setup

1. Create and activate virtual environment:

    ```bash
    uv venv
    source .venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    uv pip install -r requirements.txt
    ```

3. Create `.env` file:

    ```bash
    touch .env
    ```

4. Add your environment variables to `.env`:

    ```ini
    NOTION_API_KEY=your_notion_api_key
    OPENAI_API_KEY_=your_openai_api_key
    NOTION_ENDPOINT=https://api.notion.com/v1
    NOTION_PAGE_ID=your_notion_page_id
    ```

## Verifying Installation

1. Ensure your virtual environment is activated (you should see `(.venv)` in your prompt)

2. Verify dependencies are installed:

    ```bash
    uv pip list
    ```

3. Run the application:

    ```bash
    python app.py
    ```

## Troubleshooting

### Common Issues

1. **`uv` command not found**
   - Windows: Restart PowerShell or add uv to PATH manually
   - Linux/macOS: Restart terminal or add uv to PATH manually

2. **Virtual environment activation fails**
   - Windows: Ensure you're using PowerShell and not CMD
   - Linux/macOS: Verify the path to activate script

3. **Package installation errors**
   - Check internet connection
   - Verify requirements.txt is in the correct directory
   - Try updating uv: `uv self update`
   - For Git-related errors, ensure Git is installed and accessible from command line

4. **Swarm package installation fails**
   - Ensure Git is installed and accessible from command line
   - Try installing swarm package separately: `uv pip install git+https://github.com/openai/swarm.git`
