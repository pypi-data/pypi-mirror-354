from fastmcp import Context

# Example context helper to get the current request/session context
def get_current_context(ctx: Context) -> dict:
    """Returns information about the current MCP request/session context."""
    return {
        "request_id": ctx.request_id,
        "user": getattr(ctx, 'user', None),
        "timestamp": getattr(ctx, 'timestamp', None),
    }

# Example usage in a prompt, tool, or resource:
# def some_resource(..., ctx: Context):
#     context_info = get_current_context(ctx)
#     ... 