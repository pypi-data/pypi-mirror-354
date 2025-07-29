# Changelog

## [0.9.5]

### Fixed
- Fixed callback parameter name mismatch and added unit tests
- Improved Unicode support in JSON outputs

### Improved
- Added cost information to CLI run logs for better usage tracking
- Enhanced documentation with navigation links and fixed broken references

## [0.9.4] - 2025-06-07

### Improved
- **Code Organization**: Refactors in LLMProcess and LLMProgram
- **Configuration Flexibility**: Allow extra fields in program config
- **Test Infrastructure**: Moved pytest configs to pyproject.toml
- **Callback warning**: Removed unnecesary warnings

## [0.9.3] - 2025-06-06

See [detailed release notes](docs/release_notes/RELEASE_NOTES_0.9.3.md) for complete information.

### Added
- **Cost Control**: New `--cost-limit` option for both CLIs with proactive cost management
- **Enhanced Callbacks**: Smart parameter passing and RunResult support for budget checking
- **Improved Tool Registration**: Enhanced class method and instance method support

### Improved
- GitHub Actions security fixes and workflow enhancements
- CLI: Added `--upgrade` option to `llmproc-install-actions`
- Documentation and tool registration examples

### Breaking Changes
- **Stop Reason API**: `process.run_stop_reason` deprecated in favor of `run_result.stop_reason`

## [0.9.0] - 2025-05-28

See [detailed release notes](docs/release_notes/RELEASE_NOTES_0.9.0.md) for complete information.

### Added
- **GitHub Automation Workflows**:
  - `@llmproc /code` for automated code implementation
  - `@llmproc /ask` for question answering
  - `@llmproc /resolve` for PR conflict resolution

- **Improved CLI Experience**:
  - `llmproc`: Added `--prompt-file` option and `--json` flag for structured output
  - `llmproc-demo`: Enhanced `-p/--prompt` flag handling for flexible prompt control
    - `-p "custom prompt"`: Run custom prompt, then continue interactive
    - `-p` (without argument): Skip embedded prompt, go directly to interactive mode
    - Default behavior: Show embedded prompt with confirmation, then interactive

- **Enhanced Environment Info System** (Experimental):
  - Runtime commands support via `commands` option
  - Multiple environment variables support
  - File mapping option for virtual paths
  - Configurable base path for preloading

### Improved
- Error handling and logging improvements
- Enhanced MCP error logging with detailed diagnostic information for better debugging

### Breaking Changes
- Removed deprecated `tool_aliases` parameter in favor of ToolConfig-based aliases

## [0.8.0] - 2025-05-25

See [detailed release notes](docs/release_notes/RELEASE_NOTES_0.8.0.md) for complete information and migration guide.

### Added
- **Synchronous API Support**: New `program.start_sync()` method returns `SyncLLMProcess` for blocking operations
  - All async methods now have synchronous counterparts
  - Automatic event loop management for synchronous codebases

- **Dictionary & YAML Configuration**: Added support for Python dictionaries and YAML format
  - `LLMProgram.from_dict(config_dict)` for dynamic configuration
  - YAML configuration alternative to TOML

- **MCP Enhancements**:
  - New `MCPServerTools` class for tool registration
  - Embedded MCP server configurations directly in TOML/YAML
  - Tool description override support

- **Dual CLI**:
  - `llmproc` for single prompt execution (non-interactive)
  - `llmproc-demo` for interactive chat (previously the only CLI)

- **Instance Methods as Tools**: Register instance methods directly as tools

- **API Retry Configuration**: Configurable retry logic via environment variables

- **Spawn Tool Self-Spawning**: Create independent instances of the same program

- **Enhanced Callbacks**: Support for async callback methods and new event types

- **Write to Standard Error**: New built-in `write_stderr` tool

- **Unified ToolConfig**: Shared configuration for MCP and built-in tools

### Changed
- **Tool Configuration Naming**: New `builtin` field for tools (alongside existing `enabled`)
- **MCP Tool Registration**: Now uses the `MCPServerTools` class

### Fixed
- MCP cleanup handling during shutdown
- Improved async/sync interface reliability
- Configuration validation edge cases
- Better error handling for incorrect tool names

## [0.7.0] - 2025-05-01

Initial version tracked in this changelog.
