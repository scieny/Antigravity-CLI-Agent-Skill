from .schemas import AntigravityToolInput
from .tools import invoke_antigravity

def register(ctx):
    """
    Registers the Antigravity tool within the Hermes Agent plugin context.
    """
    ctx.register_tool(
        name="invoke_antigravity",
        description="Call the Antigravity AI coding assistant (agy) to perform complex codebase modifications, code analysis, debugging, or file creation tasks.",
        handler=invoke_antigravity,
        schema=AntigravityToolInput
    )
