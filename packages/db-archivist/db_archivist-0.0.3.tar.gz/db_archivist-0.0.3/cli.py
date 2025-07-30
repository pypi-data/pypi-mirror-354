#!/usr/bin/env python3
"""
Database Script Manager CLI
Manages database scripts across multiple repositories with deployment tracking.
"""

import click
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from consolidator import ScriptConsolidator
from repository_scanner import RepositoryScanner
from documentation_updater import DocumentationUpdater
from deployment_checker import DeploymentChecker
from db_tracker import DatabaseTracker

# Global configuration
CONFIG_FILE = "config.yaml"
DEFAULT_CONFIG = {
    "repositories": {
        "scripts_repo": "sbwb-db-scripts",
        "versions_repo": "sbwb-versions",
    },
    "projects": {
        "workflow": {
            "source_repo": "sbwb-tool-workflow-backend",
            "source_path": "database/DEV",
            "script_path": "app_workflow",
            "versions_path": "sbwb-tool-workflow",
        },
    },
    "database_tracking": {
        "enabled": True,
        "table_name": "script_execution_log",
        "view_name": "v_script_execution_status",
    },
    "environments": ["TST", "HMG", "PRD"],
}


def load_config() -> Dict:
    """Load configuration from config.yaml or create default."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    else:
        # Create default config
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
        click.echo(f"📝 Created default config file: {CONFIG_FILE}")
        click.echo("📝 Please review and update the paths in config.yaml")
        return DEFAULT_CONFIG


@click.group()
@click.version_option(version="1.0.0", prog_name="dbmanager")
def cli():
    """
    🗄️  Database Script Manager

    Manages database scripts across multiple repositories with deployment tracking.
    Consolidates scripts, wraps them in transactions, and maintains documentation.
    """
    pass


@cli.command()
@click.option(
    "--project",
    "-p",
    required=True,
    help="Project name (e.g., sbwb-basicdata-supplies)",
)
@click.option("--pi", required=True, help="PI number (e.g., gpsub-pi07)")
@click.option("--from-script", "-f", type=int, help="Starting script number (e.g., 41)")
@click.option("--to-script", "-t", type=int, help="Ending script number (e.g., 46)")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
def consolidate(
    project: str,
    pi: str,
    from_script: Optional[int],
    to_script: Optional[int],
    dry_run: bool,
):
    """
    📦 Consolidate database scripts from source repo to sbwb-db-scripts.

    Consolidates scripts from individual project repositories into the centralized
    sbwb-db-scripts repository, wrapped in transactions with database tracking.
    """
    config = load_config()

    if project not in config["projects"]:
        click.echo(
            f"❌ Project '{project}' not found in config. Available: {list(config['projects'].keys())}"
        )
        return

    consolidator = ScriptConsolidator(config)

    try:
        result = consolidator.consolidate_scripts(
            project=project,
            pi=pi,
            from_script=from_script,
            to_script=to_script,
            dry_run=dry_run,
        )

        if dry_run:
            click.echo("🔍 DRY RUN - No changes made")
            click.echo("\n📋 Would consolidate:")
            for script in result["scripts"]:
                click.echo(f"  • {script}")
            click.echo(f"\n📁 Output: {result['output_path']}")
        else:
            click.echo("✅ Consolidation completed!")
            click.echo(f"📁 Consolidated script: {result['output_path']}")
            click.echo(f"📊 Scripts included: {len(result['scripts'])}")

            # Auto-update documentation
            click.echo("\n📝 Updating documentation...")
            doc_updater = DocumentationUpdater(config)
            doc_updater.update_pi_documentation(project, pi, result["scripts"])
            click.echo("✅ Documentation updated!")

    except Exception as e:
        click.echo(f"❌ Error during consolidation: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--pi", help="PI number to check (e.g., gpsub-pi07)")
@click.option("--project", "-p", help="Specific project to check")
@click.option("--environment", "-e", help="Specific environment to check")
@click.option(
    "--check-database", is_flag=True, help="Query database for actual execution status"
)
def status(
    pi: Optional[str],
    project: Optional[str],
    environment: Optional[str],
    check_database: bool,
):
    """
    📊 Show deployment status across projects and environments.

    Displays current deployment status by comparing sbwb-db-scripts with
    sbwb-versions documentation, optionally checking database execution logs.
    """
    config = load_config()
    checker = DeploymentChecker(config)

    try:
        if pi:
            # Show status for specific PI
            status_data = checker.get_pi_status(pi, check_database=check_database)
            _display_pi_status(pi, status_data, check_database)
        elif project:
            # Show status for specific project
            status_data = checker.get_project_status(
                project, check_database=check_database
            )
            _display_project_status(project, status_data, check_database)
        else:
            # Show overall status
            status_data = checker.get_overall_status(check_database=check_database)
            _display_overall_status(status_data, check_database)

    except Exception as e:
        click.echo(f"❌ Error checking status: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--pi", required=True, help="PI number (e.g., gpsub-pi07)")
@click.option("--environment", "-e", help="Target environment for deployment report")
def deployment_report(pi: str, environment: Optional[str]):
    """
    📋 Generate deployment report for a specific PI.

    Creates a comprehensive report showing what needs to be deployed
    to each environment for the specified PI.
    """
    config = load_config()
    checker = DeploymentChecker(config)

    try:
        report = checker.generate_deployment_report(pi, environment)
        _display_deployment_report(pi, report, environment)

    except Exception as e:
        click.echo(f"❌ Error generating report: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--environment", "-e", help="Check specific environment database")
def db_status(environment: Optional[str]):
    """
    🗄️  Query database execution logs to see what scripts have been run.

    Connects to database(s) and queries the script execution log to show
    the actual execution status of database scripts.
    """
    config = load_config()

    if not config["database_tracking"]["enabled"]:
        click.echo("❌ Database tracking is disabled in config")
        return

    tracker = DatabaseTracker(config)

    try:
        if environment:
            environments = [environment]
        else:
            environments = config["environments"]

        for env in environments:
            click.echo(f"\n🗄️  Database Status - {env}")
            click.echo("=" * 50)

            status = tracker.get_execution_status(env)
            if status:
                for record in status:
                    status_icon = "✅" if record["status"] == "COMPLETED" else "⏳"
                    click.echo(
                        f"{status_icon} {record['pi_number']}/{record['project_name']}"
                    )
                    click.echo(f"   Script: {record['script_name']}")
                    click.echo(f"   Status: {record['status']}")
                    click.echo(f"   Executed: {record['execution_date']}")
                    if record["completion_date"]:
                        click.echo(f"   Completed: {record['completion_date']}")
                    click.echo()
            else:
                click.echo("📭 No execution records found")

    except Exception as e:
        click.echo(f"❌ Error querying database: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--environment", "-e", help="Setup tracking for specific environment")
def setup_tracking():
    """
    🔧 Setup database tracking table and views.

    Creates the necessary database objects for tracking script execution.
    Run this once per environment before using database tracking features.
    """
    config = load_config()
    tracker = DatabaseTracker(config)

    try:
        environments = config["environments"]

        for env in environments:
            click.echo(f"🔧 Setting up tracking for {env}...")
            tracker.setup_tracking_schema(env)
            click.echo(f"✅ Tracking setup completed for {env}")

        click.echo("\n🎉 Database tracking setup completed for all environments!")

    except Exception as e:
        click.echo(f"❌ Error setting up tracking: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--pi", required=True, help="PI number")
@click.option("--environment", "-e", required=True, help="Target environment")
@click.option("--output-dir", "-o", help="Output directory for package")
def package(pi: str, environment: str, output_dir: Optional[str]):
    """
    📦 Generate deployment package for specific PI and environment.

    Creates a deployment package containing all scripts that need to be
    executed in the specified environment for the given PI.
    """
    config = load_config()
    consolidator = ScriptConsolidator(config)

    try:
        package_path = consolidator.create_deployment_package(
            pi=pi, environment=environment, output_dir=output_dir
        )

        click.echo(f"📦 Deployment package created: {package_path}")
        click.echo("📋 Package contains:")

        # List package contents
        package_dir = Path(package_path)
        for file in package_dir.glob("*.sql"):
            click.echo(f"  • {file.name}")

    except Exception as e:
        click.echo(f"❌ Error creating package: {str(e)}")
        sys.exit(1)


@cli.command()
def scan():
    """
    🔍 Scan all configured repositories for database scripts.

    Scans all configured project repositories to discover available
    database scripts and their current status.
    """
    config = load_config()
    scanner = RepositoryScanner(config)

    try:
        results = scanner.scan_all_repositories()

        click.echo("🔍 Repository Scan Results")
        click.echo("=" * 50)

        for project, data in results.items():
            click.echo(f"\n📁 {project}")
            if data["available"]:
                click.echo(f"  Status: ✅ Available")
                click.echo(f"  Path: {data['path']}")
                click.echo(f"  Scripts: {len(data['scripts'])}")

                if data["scripts"]:
                    latest_scripts = sorted(data["scripts"])[-5:]  # Show last 5
                    click.echo("  Latest scripts:")
                    for script in latest_scripts:
                        click.echo(f"    • {script}")
            else:
                click.echo(f"  Status: ❌ Not available")
                click.echo(f"  Path: {data['path']}")
                click.echo(f"  Error: {data.get('error', 'Unknown error')}")

    except Exception as e:
        click.echo(f"❌ Error scanning repositories: {str(e)}")
        sys.exit(1)


# Helper functions for displaying status information


def _display_pi_status(pi: str, status_data: Dict, check_database: bool):
    """Display status for a specific PI."""
    click.echo(f"📊 PI Status: {pi}")
    if check_database:
        click.echo("   (with Database Verification)")
    click.echo()

    # Create table header
    header = f"{'Project':<35} {'TST':<12} {'HMG':<12} {'PRD':<12}"
    click.echo(header)
    click.echo("─" * len(header))

    for project, data in status_data.items():
        click.echo(f"{project:<35}", nl=False)

        for env in ["TST", "HMG", "PRD"]:
            env_data = data.get(env, {})
            status = "✅" if env_data.get("deployed", False) else "❌"
            if check_database:
                db_status = "✅" if env_data.get("db_confirmed", False) else "❌"
                status += f" DB:{db_status}"
            click.echo(f" {status:<12}", nl=False)

        click.echo()  # New line after each project


def _display_project_status(project: str, status_data: Dict, check_database: bool):
    """Display status for a specific project."""
    click.echo(f"📊 Project Status: {project}")
    if check_database:
        click.echo("   (with Database Verification)")
    click.echo()

    for pi, data in status_data.items():
        click.echo(f"📋 {pi}")
        for env in ["TST", "HMG", "PRD"]:
            env_data = data.get(env, {})
            status = "✅" if env_data.get("deployed", False) else "❌"
            if check_database:
                db_status = "✅" if env_data.get("db_confirmed", False) else "❌"
                status += f" DB:{db_status}"
            click.echo(f"  {env}: {status}")
        click.echo()


def _display_overall_status(status_data: Dict, check_database: bool):
    """Display overall status across all projects and PIs."""
    click.echo("📊 Overall Status")
    if check_database:
        click.echo("   (with Database Verification)")
    click.echo()

    for project, pi_data in status_data.items():
        click.echo(f"📁 {project}")
        for pi, env_data in pi_data.items():
            click.echo(f"  📋 {pi}")
            for env in ["TST", "HMG", "PRD"]:
                data = env_data.get(env, {})
                status = "✅" if data.get("deployed", False) else "❌"
                if check_database:
                    db_status = "✅" if data.get("db_confirmed", False) else "❌"
                    status += f" DB:{db_status}"
                click.echo(f"    {env}: {status}")
        click.echo()


def _display_deployment_report(pi: str, report: Dict, environment: Optional[str]):
    """Display deployment report."""
    click.echo(f"📋 Deployment Report: {pi}")
    if environment:
        click.echo(f"   Target Environment: {environment}")
    click.echo()

    # Show summary
    total_projects = len(report.get("projects", {}))
    ready_projects = len(
        [p for p in report.get("projects", {}).values() if p.get("ready", False)]
    )

    click.echo(f"📊 Summary:")
    click.echo(f"  Total Projects: {total_projects}")
    click.echo(f"  Ready to Deploy: {ready_projects}")
    click.echo()

    # Show project details
    for project, data in report.get("projects", {}).items():
        status_icon = "🚀" if data.get("ready", False) else "⏳"
        click.echo(f"{status_icon} {project}")

        if data.get("scripts"):
            click.echo(f"  Scripts to deploy: {len(data['scripts'])}")
            for script in data["scripts"][:5]:  # Show first 5
                click.echo(f"    • {script}")
            if len(data["scripts"]) > 5:
                click.echo(f"    ... and {len(data['scripts']) - 5} more")
        else:
            click.echo("  No scripts to deploy")
        click.echo()


if __name__ == "__main__":
    cli()
