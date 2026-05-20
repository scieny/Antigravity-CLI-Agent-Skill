---
name: call-antigravity
description: Invoke the Antigravity AI coding assistant (agy) to perform complex codebase modifications, code analysis, debugging, or file creation tasks.
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: ["agy"]
---

# call-antigravity

This skill allows the OpenClaw agent to invoke the **Antigravity AI coding assistant** (`agy`) to perform highly complex development and coding tasks.

## When to Use
- **Code Refactoring**: Making extensive or structural edits to multiple files.
- **Debugging**: Solving tricky runtime errors, type checker bugs, or logic errors across files.
- **File Creation**: Generating new components, boilerplate, or modules from scratch.
- **Codebase Auditing**: Reviewing project security, performance, or accessibility.

## How to Execute

To invoke Antigravity, run the `agy` command in your terminal tool with the following guidelines:

1. **Required Flags**:
   - `--dangerously-skip-permissions` / `-d` (CRITICAL: Prevents interactive prompts from blocking your background session).
   - `--print` / `-p` (Executes the prompt non-interactively and prints the response).

2. **Optional Context Flags**:
   - `--add-dir <directory_path>`: Adds the project workspace to Antigravity's context. Always specify the workspace path if the task involves local files.
   - `--continue` / `-c`: Continues the most recent conversation session.
   - `--conversation <conversation_id>`: Resumes a specific past conversation.

### Example Commands

#### A. Run a query on a project directory
```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "Analyze the codebase for potential memory leaks or performance bottlenecks."
```

#### B. Refactor a specific file
```bash
agy --dangerously-skip-permissions --add-dir "/Users/scien/dev/my-project" --print "Refactor src/utils/helper.js to use async/await instead of promises."
```

#### C. Continue the last session with follow-up instructions
```bash
agy --dangerously-skip-permissions --continue --print "Add unit tests for the changes you just made."
```

## Tips for OpenClaw
- **Parse the Output**: Antigravity returns its output in standard Markdown format. You should read the output and update your internal memory/workspace accordingly.
- **Environment Path**: Ensure `/Users/scien/.local/bin` is added to your shell's `PATH` when spawning commands so the system can locate the `agy` executable.
