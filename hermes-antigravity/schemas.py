from pydantic import BaseModel, Field
from typing import Optional

class AntigravityToolInput(BaseModel):
    prompt: str = Field(
        description="The prompt or instruction to send to the Antigravity AI coding assistant, e.g. a request to refactor, write, or debug code."
    )
    workspace_dir: Optional[str] = Field(
        None, 
        description="Absolute path to the workspace or project directory that Antigravity should analyze, edit, or build."
    )
    continue_session: Optional[bool] = Field(
        False, 
        description="Set to true to continue the last conversation session in the terminal."
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="Specify a past conversation ID to resume that specific session."
    )
