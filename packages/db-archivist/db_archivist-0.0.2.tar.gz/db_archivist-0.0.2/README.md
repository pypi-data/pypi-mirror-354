# Database Script Manager CLI

A comprehensive CLI tool for managing database scripts across multiple repositories with deployment tracking and automated documentation.

## Features

🚀 **Script Consolidation**: Automatically consolidate scripts from individual project repositories to the centralized `db-scripts` repository
🔒 **Transaction Safety**: Wrap all scripts in transactions with proper error handling
📊 **Database Tracking**: Track script execution with detailed logging in the database
📝 **Automated Documentation**: Automatically update README files in `versions` repository
📋 **Deployment Reports**: Generate comprehensive deployment status reports
🔍 **Cross-Repository Visibility**: See deployment status across all projects and environments

## Installation

### Option 1: Using uvx (Recommended)

The easiest way to use the tool is with `uvx`, which runs it directly without global installation:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Option 1a: Run directly with uvx
uvx db-archivist --help
uvx db-archivist scan

# Option 1b: Use the convenience script (shorter commands)
chmod +x db-archivist.sh
./db-archivist.sh --help
./db-archivist.sh scan
```

### Option 2: Traditional Installation

1. **Clone/Download** the tool to your local machine

2. **Install with uv**:
   ```bash
   # Install uv if needed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install the tool
   uv pip install -e .
   
   # Or install with pip
   pip install -e .
   ```

3. **Run the tool**:
   ```bash
   db-archivist --help
   ```

### Configuration

On first run, the tool will create a `config.yaml` file with default settings. Update the paths to match your repository structure:

```yaml
repositories:
  scripts_repo: "../db-scripts"
  versions_repo: "../versions"

projects:
  -basicdata:
    source_repo: "../basicdata-backend"
    source_path: "database/dev"
    script_path: "app_basicdata"
    versions_path: "basicdata"
  -tool-workflow:
    source_repo: "../tool-backend"
    source_path: "database/DEV"
    script_path: "app_tool"
    versions_path: "tool"

database_tracking:
  enabled: true
  table_name: "script_execution_log"
  view_name: "v_script_execution_status"

environments:
  - TST
  - HMG
  - PRD
```

## Usage

### 🔍 Scan Repositories

Scan all configured repositories to see available scripts:

```bash
uvx db-archivist scan
```

### 📦 Consolidate Scripts

Consolidate scripts from a project repository for a specific PI:

```bash
# Consolidate specific range of scripts
uvx db-archivist consolidate -p -basicdata-supplies --pi gpsub-pi07 --from-script 41 --to-script 46

# Consolidate all scripts (dry run first)
uvx db-archivist consolidate -p -basicdata-supplies --pi gpsub-pi07 --dry-run
```

### 📊 Check Status

Check deployment status across projects and environments:

```bash
# Status for specific PI
uvx db-archivist status --pi pi07

# Status for specific project
uvx db-archivist status -p basicdata

# Overall status with database verification
uvx db-archivist status --check-database

# Status for specific environment
uvx db-archivist status -e PRD
```

### 📋 Generate Reports

Generate deployment reports:

```bash
# Report for specific PI
uvx db-archivist deployment-report --pi pi07

# Report for specific PI and environment
uvx db-archivist deployment-report --pi pi07 -e PRD
```

### 📦 Create Deployment Packages

Create deployment packages with all necessary scripts:

```bash
uvx db-archivist package --pi pi07 -e PRD -o ./deployments
```

### 🗄️ Database Operations

Set up database tracking (run once per environment):

```bash
uvx db-archivist setup-tracking
```

Check database execution status:

```bash
# Check all environments
uvx db-archivist db-status

# Check specific environment
uvx db-archivist db-status -e TST
```

## Generated Output

### Consolidated Scripts

The tool generates consolidated scripts with:

- **Transaction wrapping** (BEGIN/COMMIT)
- **Database tracking** with execution logging
- **Error handling** and rollback on failure
- **Individual script sections** with clear headers
- **GPSUB ticket references**

Example output structure:
```
-db-scripts/
└── scripts/
    └── pi07/
        └── postgres/
            └── u/
                └── app_basicdata/
                    ├── 41-46-CONSOLIDATED.sql  # Main consolidated script
                    ├── 41-UPDATE(1439).sql
                    ├── 42-UPDATE(1525).sql
                    ├── ...
                    └── README.md  # Auto-generated documentation
```

### Documentation Updates

Automatically updates `-versions` README files with:

- **Script deployment tables**
- **GitHub links** to scripts
- **Deployment dates** per environment
- **Version tracking**

### Database Tracking

Creates tracking tables with:

```sql
-- Query execution status
SELECT * FROM script_execution_log 
WHERE pi_number = 'pi07' 
ORDER BY execution_date DESC;

-- Use the view for formatted output
SELECT * FROM v_script_execution_status 
WHERE pi_number = 'pi07';
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `scan` | Scan all repositories for scripts | `uvx db-archivist scan` |
| `consolidate` | Consolidate scripts for a PI | `uvx db-archivist consolidate -p project --pi pi07` |
| `status` | Show deployment status | `uvx db-archivist status --pi pi07` |
| `deployment-report` | Generate deployment report | `uvx db-archivist deployment-report --pi pi07` |
| `package` | Create deployment package | `uvx db-archivist package --pi pi07 -e PRD` |
| `db-status` | Check database execution logs | `uvx db-archivist db-status -e TST` |
| `setup-tracking` | Setup database tracking | `uvx db-archivist setup-tracking` |

## Example Workflow

1. **Develop scripts** in individual project repositories
2. **Scan repositories** to see available scripts:
   ```bash
   uvx db-archivist scan
   ```
3. **Consolidate scripts** for deployment:
   ```bash
   uvx db-archivist consolidate -p basicdata --pi pi07 --from-script 41 --to-script 46
   ```
4. **Check status** before deployment:
   ```bash
   uvx db-archivist status --pi pi07
   ```
5. **Deploy to TST** (manually execute the consolidated script)
6. **Verify deployment**:
   ```bash
   uvx db-archivist db-status -e TST
   ```
7. **Promote to HMG and PRD** following the same process

## Error Handling

The tool includes comprehensive error handling:

- **Validation** of repository paths and configurations
- **Rollback** on script consolidation errors
- **Connection timeouts** for database operations
- **Detailed error messages** with troubleshooting guidance

## Database Requirements

- **PostgreSQL** 9.6 or higher
- **Permissions** to create tables and views
- **Network access** to database servers

## Troubleshooting

### Common Issues

1. **Repository not found**: Check paths in `config.yaml`
2. **Permission denied**: Ensure write access to target directories
3. **Database connection failed**: Verify network access and credentials
4. **Scripts not found**: Check source repository paths and script naming

### Debug Mode

Add `--verbose` flag to any command for detailed logging:

```bash
uvx db-archivist status --pi pi07 --verbose
```

## Contributing

1. **Test changes** thoroughly with `--dry-run` flags
2. **Update documentation** for new features
3. **Follow existing code patterns** and error handling
4. **Add tests** for new functionality
