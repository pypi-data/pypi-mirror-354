from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage

mcp = FastMCP("BugBot MCP Server")

@mcp.prompt
def code_review_prompt(
    diff: str,
    file_context: str = "",
    jira_story: str = "",
    review_criteria: list[str] = [
        "correctness", "security", "error handling", "testing", "performance", "readability", "best practices", "documentation", "suggestions"
    ]
) -> str:
    """Prompt for comprehensive, parameterized code review."""
    content = (
        f"Perform a comprehensive code review of the following GitLab Merge Request diff:\n{diff}\n\n"
    )
    if file_context:
        content += f"Project/file context:\n{file_context}\n\n"
    if jira_story:
        content += f"Jira user story:\n{jira_story}\n\n"
    content += (
        "Review the code for the following criteria:\n"
        + "\n".join(f"- {c}" for c in review_criteria)
        + "\n\nOutput findings as a JSON list with fields: type, severity, file, line, message, suggestion."
    )
    return content

@mcp.prompt
def chunking_prompt() -> str:
    """Prompt for chunking large diffs."""
    return (
        "If the diff is large, break it into manageable chunks and analyze each chunk iteratively. "
        "Aggregate findings for a complete review."
    )

@mcp.prompt
def jira_crosscheck_prompt(ticket_id: str) -> str:
    """Prompt for cross-verifying MR with a Jira ticket."""
    return f"Cross-verify the MR implementation with Jira ticket {ticket_id}."

@mcp.prompt
def review_workflow_prompt() -> str:
    """Describes the recommended code review workflow for Cursor AI."""
    return (
        "1. Fetch MR metadata and diff using get_merge_request_diff.\n"
        "2. Extract Jira ticket number from MR metadata.\n"
        "3. Fetch Jira ticket details if found.\n"
        "4. Chunk and analyze the diff using code_review_prompt.\n"
        "5. Aggregate findings and suggest approve/deny.\n"
        "6. Preview findings in Cursor.\n"
        "7. Post comments to GitLab if approved.\n"
        "8. Approve or unapprove MR as needed."
    ) 