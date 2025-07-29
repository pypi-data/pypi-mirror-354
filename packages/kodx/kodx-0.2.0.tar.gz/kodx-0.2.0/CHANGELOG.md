# Changelog

All notable changes to Kodx will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-06-06

### Added

#### Repository Analysis Feature (/ask)
- **CLI Command**: New `kodx ask` command for automated repository analysis (deprecated in favor of `kodx PROGRAM_PATH`)
- **GitHub Integration**: Complete workflow for `/ask <query>` comment triggers
- **Security Model**: Clone-then-copy pattern keeps credentials out of containers
- **Context Support**: Integration with GitHub issues/PRs metadata
- **JSON Output**: Structured results with analysis, work log, and metadata

#### Enhanced CLI Structure
- **Multi-command CLI**: Converted to Click group with `run` and `ask` subcommands
- **Backward Compatibility**: Existing `kodx run` usage preserved
- **Comprehensive Help**: Detailed documentation for all commands and options
- **Configuration Options**: Support for branch selection, custom images, output files

#### Documentation & Examples
- **Complete Documentation**: README with feature overview and usage examples
- **Architecture Docs**: Detailed technical documentation in `docs/` directory
- **GitHub Workflow Setup**: Step-by-step instructions for repository integration
- **Configuration Examples**: Sample TOML files for different use cases

#### Testing Infrastructure
- **Comprehensive Test Suite**: Unit, integration, system, and performance tests
- **CLI Testing**: Argument parsing and command integration tests
- **Mocked Operations**: Repository cloning and container operation testing
- **CI/CD Ready**: GitHub Actions workflow for automated testing

### Technical Details

#### Security Enhancements
- **Credential Isolation**: Repository cloning on host with file-only container transfer
- **Access Control**: GitHub workflow limited to repository collaborators
- **Clean Environment**: Isolated Docker execution with automatic cleanup
- **No Token Leakage**: Comprehensive credential protection throughout pipeline

#### Architecture Improvements
- **Tool Minimalism**: Uses only 2 core tools (feed_chars, create_new_shell)
- **Container Management**: Enhanced DockerCodexTools with container ID access
- **Error Handling**: Robust error management and resource cleanup
- **System Prompt**: Specialized prompt for systematic code analysis

#### Dependencies
- **llmproc**: LLM process management framework
- **docker**: Container management
- **click**: CLI framework
- **fastapi + uvicorn**: PTY server components

### Migration Notes

This is the initial release of Kodx. No migration is required.

### Known Issues

- Kodx requires Docker to be running for all operations
- Repository analysis is currently read-only (no git operations in container)
- Large repositories may take longer to analyze due to container setup time

### Supported Platforms

- **Operating Systems**: macOS, Linux, Windows (with Docker)
- **Python Versions**: 3.9, 3.10, 3.11, 3.12
- **Docker**: Any recent version with container support

---

### Development

For developers and contributors:

#### Project Structure
- Modular architecture with clear separation of concerns
- Comprehensive test coverage across all components
- Type hints and docstrings throughout codebase
- Follow Unix philosophy of doing one thing well
