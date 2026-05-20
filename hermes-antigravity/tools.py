import subprocess
import json
import os
from typing import Optional

def invoke_antigravity(
    prompt: str,
    workspace_dir: Optional[str] = None,
    continue_session: Optional[bool] = False,
    conversation_id: Optional[str] = None
) -> str:
    """
    Invokes the Antigravity AI coding assistant (agy) to perform advanced development tasks.
    All handlers must return a JSON-encoded string in Hermes Agent.
    """
    # Build the agy CLI execution command
    cmd = ["agy", "--dangerously-skip-permissions"]
    
    if workspace_dir:
        cmd.extend(["--add-dir", workspace_dir])
        
    if conversation_id:
        cmd.extend(["--conversation", conversation_id])
    elif continue_session:
        cmd.append("--continue")
        
    # Append print flag along with the user prompt
    cmd.extend(["--print", prompt])
    
    try:
        # Prepare the execution environment and ensure Antigravity's local path is present
        env = os.environ.copy()
        local_bin_path = "/Users/scien/.local/bin"
        if local_bin_path not in env.get("PATH", ""):
            env["PATH"] = f"{local_bin_path}:{env.get('PATH', '')}"
            
        # Execute the process
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
            check=False
        )
        
        # Parse result status
        if result.returncode == 0:
            return json.dumps({
                "status": "success",
                "output": result.stdout
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "status": "error",
                "code": result.returncode,
                "stderr": result.stderr,
                "stdout": result.stdout
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "status": "exception",
            "error": str(e)
        }, ensure_ascii=False)
