# CLAUDE.md - Kodx Project Context

## Project Overview

Kodx is a minimal Docker-based code execution environment designed for LLM integration. It provides exactly 2 tools for LLMs to interact with containerized development environments through natural shell commands.

**Core Principle**: Follow llmproc CLI patterns exactly while adding container isolation and local directory support.

**Implementation Status**: The `kodx code`, `kodx ask`, and `kodx init` workflow commands are now fully implemented. See [docs/git-integration.md](docs/git-integration.md) for git workflow details.

## Current Architecture (Post-Refactoring)

### CLI Interface
Kodx provides **one core command with two specialized wrappers**:

- **`kodx` (core)** - Low-level, non-interactive, git-agnostic tool for custom workflows
- **`kodx ask`** - Wrapper for git-agnostic code analysis (never exports)
- **`kodx code`** - Wrapper for git-integrated implementation (auto-exports to branches)

```bash
# Core command (manual setup, flexible)
kodx --prompt "TASK" --export-dir ./output   # Git-agnostic, manual export
kodx my-program.yaml --repo-dir . --prompt "TASK"

# High-level commands (workflow-specific)
kodx ask "QUERY"              # Git-agnostic analysis, no export
kodx code "REQUEST"           # Git workflow, auto-export to branch
```

**Key Features:**
- **Core + wrappers architecture** - One flexible core tool + specialized wrappers for common workflows
- **Container isolation** - All AI work happens in Docker containers
- **Git integration** - `kodx code` creates branches automatically and supports git refs
- **Export control** - Core requires `--export-dir`, `kodx code` auto-exports, `kodx ask` never exports
- **Built-in programs** - No setup required for common tasks
- **Cost control** - Built-in spending limits across all commands
- **JSON output** - Compatible with automation (--json or --json-output-file)
- **Typer-based CLI** - Arguments validated with Pydantic models

### Project Structure
```
kodx/
├── src/kodx/
│   ├── cli.py              # Entry point using Typer
│   ├── cli_ask.py          # kodx ask subcommand
│   ├── cli_code.py         # kodx code subcommand
│   ├── models.py           # Shared CLI models (Pydantic)
│   ├── models_ask.py       # Ask command options
│   ├── models_code.py      # Code command options
│   ├── tools.py            # DockerCodexTools with 2 @register_tool methods
│   ├── codex_shell.py      # CodexShell for PTY server communication
│   ├── programs/default.yml  # Built-in default program
│   ├── git_utils.py        # Git operations for kodx code workflow
│   ├── workspace.py        # Container workspace management
│   ├── prompt_utils.py     # Shared prompt resolution helpers
│   ├── programs/           # Built-in program files
│   │   ├── ask.yaml        # Code analysis program
│   │   └── code.yaml       # Feature implementation program
│   └── __init__.py         # Package exports
├── .github/config/         # LLM programs (for workflows)
│   ├── kodx-slash-ask-program.yaml   # Code analysis program
│   └── kodx-slash-code-program.yaml  # Code implementation program
├── docs/                   # Technical documentation
├── docs/git-integration.md # Git workflow specifications
└── README.md              # User-facing documentation
```

## Tool Interface (LLM Perspective)

Kodx exposes exactly **2 tools** to LLMs:

### `feed_chars(chars: str, shell_name: str = "default", yield_time_ms: int = 1000) -> str`
Primary interface for all shell interaction:
- Execute commands: `feed_chars("ls -la")`
- Create files: `feed_chars("cat > file.py\nprint('hello')\n")`
- Send Ctrl+C: `feed_chars("\x03")`
- Run interactive programs: `feed_chars("python")`
- Control wait time: `feed_chars("long_command", yield_time_ms=5000)`
- Multiple shells: `feed_chars("echo hello", shell_name="worker")`

### `new_session(shell_name: str = "default") -> str`
Reset environment when needed:
- Fresh shell session: `new_session()`
- Clean environment state
- Return to /workspace directory
- Named sessions: `new_session("worker")` for parallel shells

## Key Design Decisions

1. **Core + wrappers design** - Core tool is low-level, wrappers add workflow features
2. **Export control** - Core doesn't auto-export (explicit `--export-dir`), wrappers handle exports appropriately
3. **Git integration levels** - Core is git-agnostic, `ask` is git-agnostic, `code` has full git workflow
4. **Follow llmproc exactly** - Program files are required, CLI patterns match
5. **Container isolation** - Each session gets clean Docker environment
6. **Local directory focus** - Simple file copying, no git clone complexity
7. **JSON automation** - Structured output for CI/CD integration

## Development Workflow

### Session Setup
- Review tool interface in `tools.py` (only 2 methods with `@register_tool`)
- Check programs in `.github/config/` directory
- Read technical docs in `docs/` directory
- See git workflow designs in `docs/git-integration.md`

### Testing Current Interface
```bash
# Install in development mode with all extras
uv sync --all-extras --group dev

# Test high-level workflow commands
kodx ask "What is this project about?"                    # Git-aware analysis
kodx ask "How does the CLI work?" --repo-dir ./src/kodx   # Specific directory
kodx code "Add comprehensive unit tests" --cost-limit 1.0 # Git workflow

# Test core command (low-level, manual setup)
kodx --prompt "Create a hello world script"              # Uses current directory, no export
kodx --repo-dir "" --prompt "Create hello world" --export-dir ./output  # Clean container, manual export

# Test with custom programs (core command)
kodx .github/config/kodx-slash-code-program.yaml --repo-dir "" --prompt "Create hello world" --export-dir ./app
kodx .github/config/kodx-slash-ask-program.yaml --repo-dir . --prompt "Analyze this project"

# Test JSON output (all commands support this)
kodx ask "Quick scan" --json
kodx code "Add tests" --json-output-file results.json
kodx --prompt "Quick scan" --json
```

### Implementation Notes

#### Docker Container Flow
1. Initialize ``DockerCodexTools`` asynchronously (`async with`) which creates the container with `sleep infinity`
2. Install dependencies (curl, fastapi, uvicorn)
3. Deploy embedded PTY server code to `/root/pty_server.py`
4. Start PTY server on localhost:1384
5. Create bash session via HTTP POST to `/open`
6. Setup `/workspace` directory
7. Ready for `feed_chars` commands

#### PTY Server Communication
- All shell interaction goes through HTTP endpoints
- PTY provides full terminal capabilities (colors, signals, interactive programs)
- Commands sent via `/write/{pid}`, output read via `/read/{pid}`
- Session cleanup via `/kill/{pid}`

#### Tool Registration
Uses llmproc's enhanced `@register_tool` decorator that supports class methods:
```python
@register_tool(
    description=(
        "Feed characters to a session's STDIN. After feeding characters, "
        "wait some amount of time, flush STDOUT/STDERR, and show the results. "
        "Note that a minimum of 250 ms is enforced, so if a smaller value is "
        "provided, it will be overridden with 250 ms."
    )
)
async def feed_chars(self, chars: str, shell_name: str = "default", yield_time_ms: int = 1000) -> str:
    # Implementation uses CodexShell.run() with configurable timeout
```

## Integration with llmproc

Kodx is built on [llmproc](https://github.com/cccntu/llmproc-private):
- Uses standard llmproc configuration (primarily YAML, also supports TOML)
- Leverages llmproc's tool registration system
- Follows llmproc CLI patterns and options
- Integrates with llmproc's provider system (Anthropic, OpenAI, etc.)

### Docker Configuration in Program Files

Program YAML files can include Docker configuration:
```yaml
model:
  name: "claude-3-5-sonnet-20241022"
  provider: "anthropic"

docker:
  image: "python:3.11"  # Optional, defaults to python:3.11
  disable_network_after_setup: true  # Optional, enhances security isolation
  setup_script: |
    pip install flask pytest
    apt-get update && apt-get install -y git
```

## Common Usage Patterns

### Specialized Wrapper Commands (Recommended)
```bash
# Code analysis (git-agnostic, never exports)
kodx ask "What is the architecture of this project?"       # Current directory
kodx ask "Review code quality" --cost-limit 0.50          # With cost control
kodx ask "Analyze specific directory" --repo-dir ./src     # Analyze specific directory

# Feature implementation (git workflow, auto-exports to branch)
kodx code "Add user authentication"                        # Creates branch automatically
kodx code "Fix failing tests" --base-ref feature-branch   # Work from specific branch
kodx code "Debug current work" --dirty                     # Include uncommitted changes
```

### Core Command (Advanced/Custom Workflows)
```bash
# Manual export control (git-agnostic)
kodx --prompt "Create a Python web app" --export-dir ./new-app
kodx --repo-dir "" --prompt "Generate API docs" --export-dir ./docs

# Custom programs with manual setup
kodx my-program.yaml --repo-dir . --prompt "Custom task" --export-dir ./output
kodx .github/config/custom.yaml --repo-dir ./src --prompt "Analyze" 

# No export (container-only work)
kodx --prompt "Test some code"                             # Changes stay in container
```

### Command Selection Guide
- **Use `kodx ask`** for: Code analysis, questions, reviews (read-only)
- **Use `kodx code`** for: Feature implementation, bug fixes (git workflow)
- **Use `kodx` (core)** for: Custom workflows, automation, non-git work

### Setup Scripts
```bash
# Execute setup script before task (via CLI)
kodx .github/config/kodx-slash-code-program.yaml --repo-dir . --setup-script setup.sh --prompt "Run tests"

# Execute setup script with network isolation for security
kodx .github/config/kodx-slash-code-program.yaml --repo-dir . --setup-script setup.sh --disable-network-after-setup --prompt "Secure analysis"

# Or define in program YAML file:
# docker:
#   setup_script: "pip install -r requirements.txt"
#   disable_network_after_setup: true  # For security isolation
```

### Development Tasks
```bash
# Create new application
kodx .github/config/kodx-slash-code-program.yaml --repo-dir "" --prompt "Create FastAPI server" --export-dir ./new-app

# Debug existing code with export
kodx .github/config/kodx-slash-code-program.yaml --repo-dir . --prompt "Fix error in cli_code.py" --export-dir ./bugfixes
```

### Local Automation
```bash
# Export for integration with other tools
kodx .github/config/kodx-slash-ask-program.yaml --repo-dir . --prompt "Generate report and fixes" --export-dir ./changes --json-output-file results.json

# Local workflow script example
#!/bin/bash
kodx .github/config/kodx-slash-ask-program.yaml --repo-dir . --prompt "Generate report" --export-dir ./changes --json-output-file results.json
cp -r changes/* .
git add . && git commit -m "Apply automated code review"
```

### LLM Tool Usage (within programs)
```python
# File operations
feed_chars("cat > script.py << EOF\nimport sys\nprint(sys.version)\nEOF")

# Package management
feed_chars("pip install requests flask")

# Process control with timeout control
feed_chars("python -c 'print(\"hello\")'")
feed_chars("long_running_command", yield_time_ms=5000)  # Wait 5 seconds
feed_chars("\x03")  # Ctrl+C

# Multiple shell sessions
new_session("worker")  # Create named session
feed_chars("background_task &", shell_name="worker")
feed_chars("foreground_task", shell_name="default")

# Reset when needed
new_session()  # Reset default session
new_session("worker")  # Reset specific session
```

## Error Handling Strategy

- **Container failures**: Clear error messages, graceful fallback
- **PTY server issues**: Health checks, automatic retries
- **Shell problems**: `new_session()` for recovery
- **Command hangs**: `feed_chars("\x03")` for interruption

## Security Model

- Each session gets isolated Docker container
- Containers auto-removed on exit
- No persistent storage by default
- PTY server only accessible from within container
- No direct host system access
- Optional network isolation after setup with `--disable-network-after-setup` for enhanced security

## Extension Guidelines

When extending Kodx:

1. **Prefer shell commands** over new tools
2. **Keep interface minimal** - can the task be done with existing tools?
3. **Follow container isolation** - don't break the security model
4. **Document in [docs/index.md](docs/index.md)** - maintain architectural documentation
5. **Test with multiple images** - ensure compatibility

## Related Files

- **[docs/index.md](docs/index.md)** - Complete technical architecture documentation
- **[README.md](README.md)** - User-facing documentation with command comparison and quick start
- **[.github/config/](.github/config/)** - LLM program files (YAML format)
- **[src/kodx/tools.py](src/kodx/tools.py)** - Core tool implementation
- **[tests/](tests/)** - Comprehensive test suite (unit, integration, system, performance)

This project maintains a Unix philosophy: do one thing well, with a minimal and composable interface.

## Development Commands

```bash
# Run tests in tiers
make test          # Fast unit tests
make test-docker   # Integration tests (requires Docker)
make test-workflows # Slow workflow tests

# Code quality
make check         # Format + lint
make format        # Auto-format code
make lint          # Check code style
```
