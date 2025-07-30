import redis
import json
import sys
from fastmcp import FastMCP
from mcp_bugbot_gitlab.gitlab_client import GitLabClient
from mcp_bugbot_gitlab.jira_client import JiraClient
from pydantic import BaseModel
from collections import defaultdict

def get_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return r
    except redis.ConnectionError:
        print("ERROR: Redis is required but not available. Exiting.")
        sys.exit(1)

mcp = FastMCP("BugBot MCP Server")
_gitlab_client = None

def get_gitlab_client():
    global _gitlab_client
    if _gitlab_client is None:
        from mcp_bugbot_gitlab.gitlab_client import GitLabClient
        _gitlab_client = GitLabClient()
    return _gitlab_client

# Helper functions for review state

def review_state_key(project_id, mr_iid):
    return f"review_state:{project_id}:{mr_iid}"

def save_review_state(project_id, mr_iid, state_dict):
    key = review_state_key(project_id, mr_iid)
    get_redis().set(key, json.dumps(state_dict))

def get_review_state(project_id, mr_iid):
    key = review_state_key(project_id, mr_iid)
    data = get_redis().get(key)
    if data:
        return json.loads(data)
    return {
        "project_id": project_id,
        "mr_iid": mr_iid,
        "state": "pending",
        "findings": [],
        "suggestion": None,
        "last_updated": None
    }

@mcp.resource("resource://mr/{project_id}/{mr_iid}/metadata")
def mr_metadata(project_id: str, mr_iid: int) -> dict:
    """Provides MR metadata as a resource."""
    mr = get_gitlab_client().get_merge_request(project_id, mr_iid)
    return {
        "id": mr.id,
        "iid": mr.iid,
        "title": mr.title,
        "author": getattr(mr.author, 'name', None),
        "state": mr.state,
        "web_url": mr.web_url,
        "created_at": mr.created_at,
        "description": mr.description,
    }

@mcp.resource("resource://mr/{project_id}/{mr_iid}/diff")
def mr_diff(project_id: str, mr_iid: int) -> dict:
    """Provides MR diff as a resource."""
    diff = get_gitlab_client().get_merge_request_diff(project_id, mr_iid)
    return {
        "project_id": project_id,
        "mr_iid": mr_iid,
        "diff": [d for d in diff],
    }

@mcp.resource("resource://jira/{ticket_id}")
def jira_ticket(ticket_id: str) -> dict:
    """Provides Jira ticket details as a resource, including additional fields for cross-verification."""
    try:
        ticket = get_gitlab_client().get_ticket(ticket_id)
        fields = ticket.fields
        # Placeholder for acceptance criteria custom field (update 'customfield_12345' as needed)
        acceptance_criteria = getattr(fields, 'customfield_12345', None)
        return {
            "id": ticket.key,
            "summary": fields.summary,
            "description": fields.description,
            "status": fields.status.name if hasattr(fields, 'status') else None,
            "priority": fields.priority.name if hasattr(fields, 'priority') else None,
            "assignee": fields.assignee.displayName if fields.assignee else None,
            "reporter": fields.reporter.displayName if hasattr(fields, 'reporter') and fields.reporter else None,
            "issue_type": fields.issuetype.name if hasattr(fields, 'issuetype') else None,
            "labels": fields.labels if hasattr(fields, 'labels') else [],
            "acceptance_criteria": acceptance_criteria,  # Update field name/ID for your Jira instance
            "linked_issues": [
                link.outwardIssue.key for link in getattr(fields, 'issuelinks', []) if hasattr(link, 'outwardIssue')
            ],
            "comments": [
                {
                    "author": c.author.displayName,
                    "body": c.body,
                    "created": c.created
                }
                for c in getattr(fields.comment, "comments", [])
            ],
            "url": f"{get_gitlab_client().server_url}/browse/{ticket.key}",
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("resource://review_state/{project_id}/{mr_iid}")
def review_state(project_id: str, mr_iid: int) -> dict:
    """Provides review state for a given MR as a resource (persisted in Redis)."""
    return get_review_state(project_id, mr_iid)

class UpdateReviewStateParams(BaseModel):
    project_id: str
    mr_iid: int
    state: dict

@mcp.tool("update_review_state")
def update_review_state(params: UpdateReviewStateParams):
    save_review_state(params.project_id, params.mr_iid, params.state)
    return {"status": "success"}

# --- MR Diff Chunking by File ---

def diff_chunk_key(project_id, mr_iid, file_path):
    return f"review_diff:{project_id}:{mr_iid}:{file_path}"

def chunk_and_store_mr_diff_by_file(project_id, mr_iid):
    """Fetch MR diff, chunk by file, and store each chunk in Redis."""
    diff = get_gitlab_client().get_merge_request_diff(project_id, mr_iid)
    file_paths = []
    for d in diff:
        file_path = d['new_path'] if 'new_path' in d else d.get('old_path', None)
        if not file_path:
            continue
        file_paths.append(file_path)
        chunk_key = diff_chunk_key(project_id, mr_iid, file_path)
        get_redis().set(chunk_key, d['diff'])
    # Update review state with chunk info
    state = get_review_state(project_id, mr_iid)
    state['diff_chunks'] = file_paths
    state['chunk_review_progress'] = {fp: None for fp in file_paths}
    save_review_state(project_id, mr_iid, state)
    return file_paths

@mcp.tool("chunk_mr_diff_by_file")
def chunk_mr_diff_by_file(params: dict):
    """Chunk the MR diff by file and store in Redis. Params: project_id, mr_iid."""
    project_id = params['project_id']
    mr_iid = params['mr_iid']
    file_paths = chunk_and_store_mr_diff_by_file(project_id, mr_iid)
    return {"file_paths": file_paths}

@mcp.resource("resource://mr/{project_id}/{mr_iid}/diff_chunk/{file_path}")
def mr_diff_chunk(project_id: str, mr_iid: int, file_path: str) -> dict:
    """Retrieve a diff chunk for a specific file from Redis."""
    chunk_key = diff_chunk_key(project_id, mr_iid, file_path)
    diff = get_redis().get(chunk_key)
    if diff:
        return {"file_path": file_path, "diff": diff.decode('utf-8')}
    return {"error": "Chunk not found"}

@mcp.resource("resource://mr/{project_id}/{mr_iid}/diff_chunks")
def mr_diff_chunks(project_id: str, mr_iid: int) -> dict:
    """List all diff chunk file paths for a given MR."""
    state = get_review_state(project_id, mr_iid)
    return {"file_paths": state.get("diff_chunks", [])}

def generate_review_summary(findings):
    if not findings:
        return (
            "Overall Summary:\n"
            "Strengths:\n- None noted.\n"
            "Concerns/Suggestions:\n- None noted.\n"
            "Recommendation: Approve."
        )
    strengths = []
    concerns = []
    suggestion_types = set()
    for f in findings:
        t = f.get("type", "")
        sev = f.get("severity", "")
        msg = f.get("message", "")
        if sev in ("info", "low") and t in ("testing", "best practice", "suggestion"):
            strengths.append(msg)
        else:
            concerns.append(msg)
            suggestion_types.add(t)
    if not concerns:
        recommendation = "Approve with minor suggestions."
    elif any(f.get("severity") == "high" for f in findings):
        recommendation = "Request changes due to high-severity issues."
    else:
        recommendation = "Approve with suggestions."
    summary = "Overall Summary:\n"
    summary += "Strengths:\n" + ("- " + "\n- ".join(strengths) if strengths else "- None noted.") + "\n"
    summary += "Concerns/Suggestions:\n" + ("- " + "\n- ".join(concerns) if concerns else "- None noted.") + "\n"
    summary += f"Recommendation: {recommendation}"
    return summary

def _aggregate_review_findings_impl(params: dict):
    project_id = params["project_id"]
    mr_iid = params["mr_iid"]
    state = get_review_state(project_id, mr_iid)
    chunk_progress = state.get("chunk_review_progress", {})
    all_findings = []
    for findings in chunk_progress.values():
        if findings:
            all_findings.extend(findings)
    # Deduplicate by (file, line, message)
    seen = set()
    deduped = []
    for f in all_findings:
        key = (f.get("file"), f.get("line"), f.get("message"))
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    # Generate summary
    summary = generate_review_summary(deduped)
    # Store in main review state
    state["findings"] = deduped
    state["summary"] = summary
    save_review_state(project_id, mr_iid, state)
    return {"findings": deduped, "summary": summary}

@mcp.tool("aggregate_review_findings")
def aggregate_review_findings(params: dict):
    """Aggregate findings for all diff chunks in an MR, deduplicate, and store in review state. Also generate a summary."""
    return _aggregate_review_findings_impl(params)

def _preview_review_findings_impl(params: dict):
    project_id = params["project_id"]
    mr_iid = params["mr_iid"]
    state = get_review_state(project_id, mr_iid)
    findings = state.get("findings", [])
    suggestion = state.get("suggestion", None)
    return {"findings": findings, "suggestion": suggestion, "state": state.get("state", "pending")}

@mcp.tool("preview_review_findings")
def preview_review_findings(params: dict):
    """Preview the aggregated findings and review suggestion for an MR."""
    return _preview_review_findings_impl(params)

def _post_aggregated_findings_to_gitlab_impl(params: dict):
    project_id = params["project_id"]
    mr_iid = params["mr_iid"]
    state = get_review_state(project_id, mr_iid)
    if state.get("state") != "approved":
        return {"error": "Review is not approved. Cannot post findings."}
    findings = state.get("findings", [])
    summary = state.get("summary", None)
    results = []
    # Post the summary as a top-level comment first
    if summary:
        summary_body = f"OVERALL REVIEW SUMMARY\n\n{summary}"
        try:
            note = get_gitlab_client().post_comment(project_id, mr_iid, summary_body)
            results.append({"type": "summary", "status": "success", "id": note.id})
        except Exception as e:
            results.append({"type": "summary", "status": "error", "error": str(e)})
    # Post each finding as before
    for finding in findings:
        file = finding.get("file", "")
        line = finding.get("line", "")
        message = finding.get("message", "")
        suggestion = finding.get("suggestion", "")
        body = f"{file}:{line}: {message}\nSuggestion: {suggestion}" if suggestion else f"{file}:{line}: {message}"
        try:
            note = get_gitlab_client().post_comment(project_id, mr_iid, body)
            results.append({"file": file, "line": line, "status": "success", "id": note.id})
        except Exception as e:
            results.append({"file": file, "line": line, "status": "error", "error": str(e)})
    return {"results": results}

@mcp.tool("post_aggregated_findings_to_gitlab")
def post_aggregated_findings_to_gitlab(params: dict):
    """Post all aggregated findings and the overall summary to GitLab as MR comments, only if review is approved."""
    return _post_aggregated_findings_to_gitlab_impl(params)

@mcp.tool("start_full_project_review")
def start_full_project_review(params: dict):
    """Explicitly start a full project review by listing all files and caching in Redis. Not part of standard MR review."""
    project_id = params["project_id"]
    ref = params.get("ref", "main")
    try:
        files = get_gitlab_client().list_project_files(project_id, path="", recursive=True)
        # Cache file list in Redis under a separate key
        key = f"full_project_review:{project_id}:{ref}:files"
        get_redis().set(key, json.dumps(files))
        # Update review state with a flag
        state = get_review_state(project_id, 0)  # Use mr_iid=0 for project-wide review
        state["full_project_review"] = True
        state["full_project_review_files"] = files
        save_review_state(project_id, 0, state)
        warning = None
        if len(files) > 1000:
            warning = f"Warning: Project is large ({len(files)} files). Full review may be slow."
        return {"files": files, "file_count": len(files), "warning": warning}
    except Exception as e:
        return {"error": str(e)} 