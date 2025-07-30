# MCP BugBot GitLab

## Installation (via PyPI)

Install the MCP BugBot GitLab package from PyPI:

```bash
pip install mcp-bugbot-gitlab
```

> If you use a virtual environment (recommended):
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install mcp-bugbot-gitlab
> ```

---

## Overview

MCP BugBot GitLab is a Python-based MCP server designed to automate and streamline AI-powered code review for GitLab Merge Requests (MRs). It enables Cursor AI to view code and MRs, facilitating AI-assisted code reviews, Jira cross-verification, and professional feedback.

---

## Configuration

You can configure MCP BugBot GitLab using environment variables, either directly or via your Cursor MCP configuration.

**Required:**
- `GITLAB_URL`: Your GitLab server URL (e.g., `https://gitlab.com`)
- `GITLAB_TOKEN`: Your GitLab Personal Access Token

**Optional:**
- `GITLAB_SSL_NO_VERIFY`: Set to `1` to disable SSL verification (for self-hosted GitLab)
- `GITLAB_USER`: The GitLab username (if needed for API calls)
- `JIRA_SERVER_URL`, `JIRA_TOKEN`, `JIRA_PROJECT_KEY`: For Jira integration/cross-verification

---

## Using with Cursor AI

1. **Register the MCP Server with Cursor**

   Add the following to your `~/.cursor/mcp.json`:

   ```json
   {
     "mcpServers": {
       "gitlab-bugbot": {
         "command": "/path/to/your/python",
         "args": ["-m", "mcp_bugbot_gitlab.server"],
         "description": "GitLab BugBot MCP server using venv Python",
         "env": {
           "GITLAB_URL": "https://gitlab.example.com",
           "GITLAB_TOKEN": "your_gitlab_token",
           "GITLAB_SSL_NO_VERIFY": "1",
           "GITLAB_USER": "your_gitlab_username",
           "JIRA_SERVER_URL": "https://jira.example.com",
           "JIRA_TOKEN": "your_jira_token",
           "JIRA_PROJECT_KEY": "YOURPROJECT"
         }
       }
     }
   }
   ```

   - Adjust the `"command"` path to your Python interpreter (e.g., from a virtualenv).
   - Set all environment variables as needed for your environment.

2. **Start Cursor**

   - Open Cursor and ensure the MCP server is registered.
   - GitLab BugBot tools will be available in the Cursor tool interface.

---

## Running the Server Manually

You can also start the server directly (for development):

```bash
python -m mcp_bugbot_gitlab.server
```

---

## Development

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

---

## Release & PyPI Publishing

- Releases are published to PyPI via GitHub Actions using OIDC (trusted publishing).
- To publish a new version, push a tag like `v1.2.3` to GitHub.
- See `.github/workflows/pypi-publish.yml` for details.

---

## License

MIT