from fastmcp import FastMCP
from pydantic import BaseModel
from typing import List, Dict
from mcp_bugbot_gitlab.gitlab_client import GitLabClient

mcp = FastMCP("BugBot MCP Server")

gitlab_client = GitLabClient()

class PingParams(BaseModel):
    message: str

@mcp.tool("ping")
def ping(params: PingParams):
    """Simple ping tool for testing MCP server registration."""
    return {"response": f"pong: {params.message}"}

class GetMRParams(BaseModel):
    project_id: str
    mr_iid: int

@mcp.tool("get_merge_request")
def get_merge_request(params: GetMRParams):
    """Fetch a merge request from GitLab and return basic info."""
    try:
        mr = gitlab_client.get_merge_request(params.project_id, params.mr_iid)
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
    except Exception as e:
        return {"error": str(e)}

class GetMRDiffParams(BaseModel):
    project_id: str
    mr_iid: int

@mcp.tool("get_merge_request_diff")
def get_merge_request_diff(params: GetMRDiffParams):
    """Fetch a merge request's metadata and diff from GitLab."""
    try:
        mr = gitlab_client.get_merge_request(params.project_id, params.mr_iid)
        diff = gitlab_client.get_merge_request_diff(params.project_id, params.mr_iid)
        return {
            "metadata": {
                "id": mr.id,
                "iid": mr.iid,
                "title": mr.title,
                "author": getattr(mr.author, 'name', None),
                "state": mr.state,
                "web_url": mr.web_url,
                "created_at": mr.created_at,
                "description": mr.description,
            },
            "diff": [d for d in diff],
        }
    except Exception as e:
        return {"error": str(e)}

class GetUserByUsernameParams(BaseModel):
    username: str

@mcp.tool("get_user_by_username")
def get_user_by_username(params: GetUserByUsernameParams):
    """Get a GitLab user by username."""
    try:
        user = gitlab_client.get_user_by_username(params.username)
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "state": user.state,
                "web_url": user.web_url,
            }
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

class ReviewComment(BaseModel):
    file: str
    line: int
    message: str

class PostReviewCommentsParams(BaseModel):
    project_id: str
    mr_iid: int
    comments: List[ReviewComment]

@mcp.tool("post_review_comments")
def post_review_comments(params: PostReviewCommentsParams):
    """Post a list of review comments to a GitLab MR."""
    results = []
    for comment in params.comments:
        try:
            # Format the comment body with file and line info
            body = f"{comment.file}:{comment.line}: {comment.message}"
            note = gitlab_client.post_comment(params.project_id, params.mr_iid, body)
            results.append({"file": comment.file, "line": comment.line, "status": "success", "id": note.id})
        except Exception as e:
            results.append({"file": comment.file, "line": comment.line, "status": "error", "error": str(e)})
    return {"results": results}

class GetProjectByPathParams(BaseModel):
    path: str

@mcp.tool("get_project_by_path")
def get_project_by_path(params: GetProjectByPathParams):
    """Fetch a GitLab project by its path (namespace/name)."""
    try:
        project = gitlab_client.get_project_by_path(params.path)
        return {
            "id": project.id,
            "name": project.name,
            "path_with_namespace": project.path_with_namespace,
            "web_url": project.web_url,
        }
    except Exception as e:
        return {"error": str(e)}

class GetMRChangesParams(BaseModel):
    project_id: str
    mr_iid: int

@mcp.tool("get_merge_request_changes")
def get_merge_request_changes(params: GetMRChangesParams):
    """Fetch the actual file changes (patches) for a merge request from GitLab."""
    try:
        changes = gitlab_client.get_merge_request_changes(params.project_id, params.mr_iid)
        return {"changes": changes}
    except Exception as e:
        return {"error": str(e)}

class GetMRCommentsParams(BaseModel):
    project_id: str
    mr_iid: int

@mcp.tool("get_merge_request_comments")
def get_merge_request_comments(params: GetMRCommentsParams):
    """Fetch all comments (notes) for a merge request from GitLab."""
    try:
        comments = gitlab_client.get_merge_request_comments(params.project_id, params.mr_iid)
        return {"comments": [
            {
                "id": c.id,
                "author": getattr(c.author, 'username', None),
                "body": c.body,
                "created_at": c.created_at
            } for c in comments
        ]}
    except Exception as e:
        return {"error": str(e)}

class ListProjectFilesParams(BaseModel):
    project_id: str
    path: str = ""
    recursive: bool = True

@mcp.tool("list_project_files")
def list_project_files(params: ListProjectFilesParams):
    """List all files in a GitLab project (optionally recursively)."""
    try:
        files = gitlab_client.list_project_files(params.project_id, params.path, params.recursive)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

class GetFileContentParams(BaseModel):
    project_id: str
    file_path: str
    ref: str = "main"

@mcp.tool("get_file_content")
def get_file_content(params: GetFileContentParams):
    """Fetch the content of a file in a GitLab project."""
    try:
        content = gitlab_client.get_file_content(params.project_id, params.file_path, params.ref)
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

class ListGroupProjectsParams(BaseModel):
    group_name: str

@mcp.tool("list_group_projects")
def list_group_projects(params: ListGroupProjectsParams):
    """List all projects in a GitLab group."""
    try:
        projects = gitlab_client.list_group_projects(params.group_name)
        return {"projects": projects}
    except Exception as e:
        return {"error": str(e)}

class ListOpenMRsParams(BaseModel):
    project_id: str

@mcp.tool("list_open_merge_requests")
def list_open_merge_requests(params: ListOpenMRsParams):
    """List all open merge requests for a project."""
    try:
        mrs = gitlab_client.list_open_merge_requests(params.project_id)
        return {"merge_requests": mrs}
    except Exception as e:
        return {"error": str(e)}

class ListGroupProjectsRecursiveParams(BaseModel):
    group_name: str

@mcp.tool("list_group_projects_recursive")
def list_group_projects_recursive(params: ListGroupProjectsRecursiveParams):
    """List all projects in a GitLab group and its subgroups recursively."""
    try:
        projects = gitlab_client.list_group_projects_recursive(params.group_name)
        return {"projects": projects}
    except Exception as e:
        return {"error": str(e)}

class ListGroupOpenMRsParams(BaseModel):
    group_name: str

@mcp.tool("list_group_open_merge_requests")
def list_group_open_merge_requests(params: ListGroupOpenMRsParams):
    """List all open merge requests in a group and its subgroups."""
    try:
        mrs = gitlab_client.list_group_open_merge_requests(params.group_name)
        return {"merge_requests": mrs}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run() 