# draftmk

`draftmk` is an advanced command-line tool that automates the setup, management, and deployment of MkDocs-based documentation projects using Docker. It streamlines local previews, live editing, and environment setup. It also supports CI/CD automation with flexible repository integration and configuration scaffolding for both public and internal documentation views.

## Features

- One-command environment bootstrap with optional Git initialization
- CI-friendly flags: `--no-git` to skip Git setup, `--repo` to link existing repositories
- Automatic port assignment in the range 3000-3999 (avoids conflicts)
- Colorful CLI output for improved user experience
- Docker Compose configuration scaffolded from templates
- Friendly preview logs and automatic browser launching
- Supports seamless integration into CI pipelines
- Supports remote Copier templates
- Automatic version checking to notify about updates

## Quick Start

```bash
draftmk init my-docs
cd my-docs
draftmk up
```

Make sure Docker and Python ≥ 3.9 are installed.

This scaffolds your project, starts Docker services, and opens the frontend in your browser. Edit content in `docs/index.md` and see it live instantly!

## Installation

Install from PyPI:

```bash
pip install draftmk
```

## Commands

### `init`

Bootstraps a new DraftMk project.

```bash
draftmk init [<directory>] [--no-git] [--repo <org/repo>] [--force] [--force-git] [--template <path-or-url>]
```

- If no `<directory>` is given, user is prompted (default is `draftmk-docs`)
- Project names must use lowercase letters, numbers, and hyphens only (e.g., draftmk-docs123)
- `--repo` specifies the repository name in format "org/repo" (defaults to the directory name)
- Scaffolds project using a Copier template (all configuration and file generation is handled by the template)
- `--force` bypasses directory emptiness check
- `--force-git` initializes Git even if a .git directory exists

You can override the default Copier template with `--template`.
See [Project Scaffolding with Copier](#project-scaffolding-with-copier).

### `up`

Initializes the project (if needed), pulls images, builds containers, and opens the browser.

```bash
draftmk up [--no-browser]
```

- Runs `init` automatically if `.env` is missing
- `--no-browser`: Do not open the frontend automatically

### `preview`

Starts the full environment and shows Docker logs.

```bash
draftmk preview [--open]
```

- Assumes project is already initialized
- `--open`: Launches the frontend in your default browser

### `view`

Launches the frontend in your browser using the port defined in `.env`.

```bash
draftmk view [--print]
```

- `--print`: Only print the preview URL instead of launching the browser

### `logs`

Tails the last 50 lines of the `.draftmk/logs/draftmk.log` file.

```bash
draftmk logs
```

### `stop`

Stops all DraftMk-related Docker containers.

```bash
draftmk stop
```

### `status`

Shows the running status of all containers.

```bash
draftmk status
```

## Error Handling and Logging

DraftMk implements comprehensive error handling and logging:

- All operations are logged to `.draftmk/logs/draftmk.log`
- Colorful terminal output using the Rich library provides clear status indicators
- Dependency checks ensure Docker and Docker Compose are installed
- Graceful handling of keyboard interrupts (Ctrl+C)
- Detailed error messages for common issues:
  - Missing dependencies
  - Port conflicts
  - Directory permission issues
  - Template errors

The `logs` command provides easy access to the log file for troubleshooting:

```bash
draftmk logs
```

## Project Name Validation

DraftMk enforces strict project name validation:

- Names must use lowercase letters, numbers, and hyphens only
- Names must follow the pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Examples of valid names: `draftmk-docs`, `my-project-123`
- Examples of invalid names: `Docs` (uppercase), `docs_project` (underscore), `my-` (trailing hyphen)

This ensures compatibility with Docker container naming, Git repositories, and URL paths.

## .env Handling and Port Assignment

During `init`, DraftMk discovers available ports in the range 3000-3999 and passes these values (along with other variables) to the Copier template. The Copier template is entirely responsible for generating the `.env` file and all configuration scaffolding. The actual content and structure of `.env` is determined by the Copier template in use.

## Directory Structure

```
.
├── .draftmk/
│   ├── config/
│   │   ├── mkdocs.internal.yml
│   │   └── mkdocs.public.yml
│   ├── site/
│   │   ├── public/
│   │   └── internal/
│   ├── logs/
│   │   └── draftmk.log
├── docs/
│   └── index.md
├── .env
├── docker-compose.yml
```

## Git Initialization Logic

- `--no-git`: Skip Git setup entirely
- `--force-git`: Force Git init even if `.git` exists
- If neither flag is set:
  - CLI prompts user interactively (default is yes)
  - Initializes on `main` branch

## Usage Examples for CI Automation

DraftMk supports seamless integration into CI pipelines with several CI-friendly options:

To bootstrap a project without Git initialization (useful in CI pipelines):

```bash
draftmk init --no-git
```

For automated documentation builds in CI:

```bash
# Example CI workflow
draftmk init --no-git --repo your-org/your-repo
draftmk up --no-browser
# Run additional build or deployment steps
```

To bootstrap and link to an existing repository:

```bash
draftmk init --repo yourusername/yourrepo
```

## Docker Images

DraftMk uses pre-built Docker images hosted on Docker Hub. These images are referenced in the docker-compose.yml file generated by the Copier template:

- **Backend**: [`jonmatum/draftmk-backend`](https://hub.docker.com/r/jonmatum/draftmk-backend) - Handles the MkDocs build process
- **Frontend**: [`jonmatum/draftmk-frontend`](https://hub.docker.com/r/jonmatum/draftmk-frontend) - Serves the web interface
- **Preview**: [`jonmatum/draftmk-preview`](https://hub.docker.com/r/jonmatum/draftmk-preview) - Provides live preview functionality

## Project Scaffolding with Copier

DraftMk scaffolds projects using [Copier](https://copier.readthedocs.io/) during `draftmk init`. The default template is [`gh:jonmatum/draftmk-copier-templates`](https://github.com/jonmatum/draftmk-copier-templates).

All configuration and file generation—including `.env`, `docs/index.md`, and all MkDocs config files—is handled exclusively by the Copier template. DraftMk CLI does not generate or modify these files directly.

To override the template, pass `--template` with a Copier-compatible repo or path.

This enables full customization of how your documentation project is initialized.

- Copier variables passed to the template include:
  ```yaml
  project_name: "DraftMk Docs"
  repo_name: "your-org/your-repo"
  site_url: "https://example.com"
  vite_env: "production"
  frontend_port: <dynamically assigned>
  backend_port: <dynamically assigned>
  preview_port: <dynamically assigned>
  ```
- DraftMk pre-fills dynamic ports and environment for the template using Copier's data injection.

Make sure the template repo is tagged if you're using a versioned reference.

## Requirements

- Python ≥ 3.9
- Docker
- Docker Compose

### Python Dependencies
- rich (≥14.0.0)
- psutil (≥7.0.0)
- copier (≥9.0.0)

## Dependency Checking

DraftMk performs automatic dependency checking before executing commands:

```bash
def check_prerequisites():
    required = ["docker", "docker-compose"]
    for cmd in required:
        if not shutil.which(cmd):
            logger.error(f"Missing required command: {cmd}")
            raise MissingDependencyError(f"Required command '{cmd}' not found.")
```

This ensures that Docker and Docker Compose are installed before attempting any operations, providing clear error messages if dependencies are missing.

## Port Discovery Algorithm

DraftMk uses a sophisticated port discovery algorithm to find available ports:

- Scans for open ports in the range 3000-3999
- Uses `psutil` to check for listening ports
- Falls back to socket binding tests if permission issues occur
- Ensures no port conflicts between frontend, backend, and preview services
- Passes discovered ports to the Copier template for configuration

## Command Execution Flow

The typical command execution flow in DraftMk is:

1. **Dependency Check**: Verify Docker and Docker Compose are installed
2. **Environment Setup**: Create necessary directories and log files
3. **Configuration**: Generate or read configuration files
4. **Docker Operations**: Pull images, start containers, or check status
5. **User Feedback**: Provide colorful terminal output and browser launching

## Version Checking

DraftMk automatically checks for updates when run. If a newer version is available, it will display a notification with upgrade instructions. This check is performed silently and will not interrupt normal operation if it fails.

## Template Source

As of the latest version, DraftMk exclusively uses the [public Copier template repository](https://github.com/jonmatum/draftmk-copier-templates) for project scaffolding by default.

- Custom templates can still be provided via `--template`
- Default behavior uses: `gh:jonmatum/draftmk-copier-templates`

## License

[MIT](LICENSE) © [Jonatan Mata](https://jonmatum.dev)

---

```bash
echo "Pura Vida & Happy Coding!";
```
