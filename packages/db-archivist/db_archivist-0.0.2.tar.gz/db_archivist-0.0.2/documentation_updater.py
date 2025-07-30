"""
Documentation Updater
Updates documentation in the sbwb-versions repository.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class DocumentationUpdater:
    def __init__(self, config: Dict):
        self.config = config
        self.versions_repo = (
            Path(config["repositories"]["versions_repo"]).expanduser().absolute()
        )

    def update_pi_documentation(self, project_name: str, pi: str, scripts: List[str]):
        """
        Update the README.md file in sbwb-versions for a specific project and PI.

        Args:
            project_name: Name of the project
            pi: PI number
            scripts: List of script filenames
        """
        if project_name not in self.config["projects"]:
            raise ValueError(f"Project '{project_name}' not found in configuration")

        project_config = self.config["projects"][project_name]
        versions_path = project_config["versions_path"]
        readme_path = self.versions_repo / versions_path / "README.md"

        if not readme_path.exists():
            raise FileNotFoundError(f"README.md not found: {readme_path}")

        # Read current README
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update the scripts table
        updated_content = self._update_scripts_table(content, pi, scripts)

        # Write back to file
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

    def mark_deployment(
        self,
        project_name: str,
        pi: str,
        scripts: List[str],
        environment: str,
        deployment_date: str = None,
    ):
        """
        Mark scripts as deployed in the documentation.

        Args:
            project_name: Name of the project
            pi: PI number
            scripts: List of script filenames
            environment: Environment (TST, HMG, PRD)
            deployment_date: Deployment date (defaults to today)
        """
        if deployment_date is None:
            deployment_date = datetime.now().strftime("%y-%m-%d")

        if project_name not in self.config["projects"]:
            raise ValueError(f"Project '{project_name}' not found in configuration")

        project_config = self.config["projects"][project_name]
        versions_path = project_config["versions_path"]
        readme_path = self.versions_repo / versions_path / "README.md"

        if not readme_path.exists():
            raise FileNotFoundError(f"README.md not found: {readme_path}")

        # Read current README
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update deployment dates for scripts
        updated_content = self._update_deployment_dates(
            content, scripts, environment, deployment_date, pi
        )

        # Write back to file
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

    def _update_scripts_table(self, content: str, pi: str, scripts: List[str]) -> str:
        """Update the scripts table section in README."""
        # Find the scripts table section
        scripts_section_pattern = r"## Scripts de banco\s*\n\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n\s*\|[-\s|]+\|\s*\n(.*?)(?=\n##|\Z)"

        match = re.search(scripts_section_pattern, content, re.DOTALL)
        if not match:
            # If no scripts table found, add one
            return self._add_scripts_table(content, pi, scripts)

        # Extract existing table rows
        table_content = match.group(1)
        existing_rows = []

        for line in table_content.split("\n"):
            line = line.strip()
            if line and line.startswith("|") and "UPDATE" in line:
                existing_rows.append(line)

        # Add new scripts
        new_rows = []
        for script in scripts:
            script_name = script.replace(".sql", "")
            github_link = self._generate_github_link(script, pi)
            new_row = f"| [{script}]({github_link}) | - | - | - |"

            # Check if this script already exists
            script_exists = any(script_name in row for row in existing_rows)
            if not script_exists:
                new_rows.append(new_row)

        # Combine existing and new rows
        all_rows = existing_rows + new_rows

        # Sort rows by script number
        all_rows.sort(key=lambda x: self._extract_script_number_from_row(x))

        # Rebuild table
        table_header = "| Script          | TST      | HMG      | PRD      |\n| --------------- | -------- | -------- | -------- |"
        new_table_content = table_header + "\n" + "\n".join(all_rows)

        # Replace the table in content
        return (
            content[: match.start()]
            + "## Scripts de banco\n\n"
            + new_table_content
            + content[match.end() :]
        )

    def _update_deployment_dates(
        self,
        content: str,
        scripts: List[str],
        environment: str,
        deployment_date: str,
        pi: str,
    ) -> str:
        """Update deployment dates for specific scripts."""
        lines = content.split("\n")
        updated_lines = []

        env_column = {"TST": 2, "HMG": 3, "PRD": 4}
        column_index = env_column.get(environment)

        if column_index is None:
            raise ValueError(f"Invalid environment: {environment}")

        for line in lines:
            updated_line = line

            # Check if this line contains one of our scripts
            for script in scripts:
                script_name = script.replace(".sql", "")
                if script_name in line and line.strip().startswith("|"):
                    # Parse the table row
                    columns = [col.strip() for col in line.split("|")]
                    if len(columns) > column_index:
                        # Update the deployment date
                        columns[column_index] = f" {deployment_date} "
                        updated_line = "|".join(columns)
                    break

            updated_lines.append(updated_line)

        return "\n".join(updated_lines)

    def _add_scripts_table(self, content: str, pi: str, scripts: List[str]) -> str:
        """Add a new scripts table if one doesn't exist."""
        table_rows = []

        for script in scripts:
            github_link = self._generate_github_link(script, pi)
            table_rows.append(f"| [{script}]({github_link}) | - | - | - |")

        scripts_table = f"""
## Scripts de banco

| Script          | TST      | HMG      | PRD      |
| --------------- | -------- | -------- | -------- |
{chr(10).join(table_rows)}
"""

        # Find a good place to insert the table (after version table)
        version_table_pattern = r"## Versões\s*\n.*?\n\s*\n"
        match = re.search(version_table_pattern, content, re.DOTALL)

        if match:
            # Insert after version table
            insert_pos = match.end()
            return content[:insert_pos] + scripts_table + "\n" + content[insert_pos:]
        else:
            # Append at the end of historical section
            history_pattern = r"# Histórico\s*\n"
            match = re.search(history_pattern, content)
            if match:
                insert_pos = match.end()
                return (
                    content[:insert_pos] + scripts_table + "\n" + content[insert_pos:]
                )

        # If no good place found, append to end
        return content + "\n" + scripts_table

    def _generate_github_link(self, script: str, pi: str) -> str:
        """Generate GitHub link for a script."""
        # This would need to be customized based on your GitHub repository structure
        base_url = "https://github.com/petrobrasbr/sbwb-db-scripts/blob/main/scripts"
        return f"{base_url}/{pi}/postgres/usbwb/app_supplies/{script}"

    def _extract_script_number_from_row(self, row: str) -> int:
        """Extract script number from a table row for sorting."""
        # Extract number from patterns like "| 05-UPDATE..."
        match = re.search(r"\|\s*\[?(\d+)[-_]", row)
        if match:
            return int(match.group(1))
        return 999  # Put unmatched rows at the end

    def get_deployment_status(self, project_name: str) -> Dict:
        """
        Get current deployment status from the README file.

        Args:
            project_name: Name of the project

        Returns:
            Dict with deployment status for each script and environment
        """
        if project_name not in self.config["projects"]:
            raise ValueError(f"Project '{project_name}' not found in configuration")

        project_config = self.config["projects"][project_name]
        versions_path = project_config["versions_path"]
        readme_path = self.versions_repo / versions_path / "README.md"

        if not readme_path.exists():
            return {}

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        return self._parse_deployment_status(content)

    def _parse_deployment_status(self, content: str) -> Dict:
        """Parse deployment status from README content."""
        status = {}

        # Find the scripts table
        scripts_section_pattern = r"## Scripts de banco\s*\n\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\n\s*\|[-\s|]+\|\s*\n(.*?)(?=\n##|\Z)"

        match = re.search(scripts_section_pattern, content, re.DOTALL)
        if not match:
            return status

        table_content = match.group(1)

        for line in table_content.split("\n"):
            line = line.strip()
            if (
                line
                and line.startswith("|")
                and ("UPDATE" in line or "CREATE" in line or "SCHEMA" in line)
            ):
                columns = [col.strip() for col in line.split("|")]
                if len(columns) >= 5:
                    script_match = re.search(r"\[(.*?)\]", columns[1])
                    if script_match:
                        script_name = script_match.group(1)
                        status[script_name] = {
                            "TST": columns[2].strip()
                            if columns[2].strip() != "-"
                            else None,
                            "HMG": columns[3].strip()
                            if columns[3].strip() != "-"
                            else None,
                            "PRD": columns[4].strip()
                            if columns[4].strip() != "-"
                            else None,
                        }

        return status
