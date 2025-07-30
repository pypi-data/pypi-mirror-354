"""
Repository Scanner
Scans project repositories to discover available database scripts.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional


class RepositoryScanner:
    def __init__(self, config: Dict):
        self.config = config

    def scan_all_repositories(self) -> Dict:
        """
        Scan all configured project repositories for database scripts.

        Returns:
            Dict mapping project names to their scan results
        """
        results = {}

        for project_name, project_config in self.config["projects"].items():
            try:
                results[project_name] = self.scan_project_repository(project_name)
            except Exception as e:
                results[project_name] = {
                    "available": False,
                    "error": str(e),
                    "path": project_config.get("source_repo", "N/A"),
                    "scripts": [],
                }

        return results

    def scan_project_repository(self, project_name: str) -> Dict:
        """
        Scan a specific project repository for database scripts.

        Args:
            project_name: Name of the project to scan

        Returns:
            Dict with scan results
        """
        if project_name not in self.config["projects"]:
            raise ValueError(f"Project '{project_name}' not found in configuration")

        project_config = self.config["projects"][project_name]
        source_repo = Path(project_config["source_repo"]).expanduser().absolute()
        source_path = source_repo / project_config["source_path"]

        if not source_path.exists():
            return {
                "available": False,
                "error": f"Source path not found: {source_path}",
                "path": str(source_path),
                "scripts": [],
            }

        # Find SQL scripts
        scripts = self._find_sql_scripts(source_path)

        return {
            "available": True,
            "path": str(source_path),
            "scripts": scripts,
            "script_count": len(scripts),
            "latest_scripts": self._get_latest_scripts(scripts, 5),
        }

    def get_scripts_in_range(
        self,
        project_name: str,
        from_script: Optional[int] = None,
        to_script: Optional[int] = None,
    ) -> List[str]:
        """
        Get scripts in a specific range for a project.

        Args:
            project_name: Name of the project
            from_script: Starting script number (optional)
            to_script: Ending script number (optional)

        Returns:
            List of script filenames
        """
        scan_result = self.scan_project_repository(project_name)

        if not scan_result["available"]:
            return []

        scripts = scan_result["scripts"]

        if from_script is not None or to_script is not None:
            filtered_scripts = []
            for script in scripts:
                script_num = self._extract_script_number(script)
                if script_num is not None:
                    if from_script is not None and script_num < from_script:
                        continue
                    if to_script is not None and script_num > to_script:
                        continue
                    filtered_scripts.append(script)
            return filtered_scripts

        return scripts

    def _find_sql_scripts(self, source_path: Path) -> List[str]:
        """Find all SQL script files in the given path."""
        if not source_path.exists():
            return []

        sql_files = []
        for file in source_path.glob("*.sql"):
            if file.is_file():
                sql_files.append(file.name)

        # Sort files naturally by script number
        sql_files.sort(key=lambda x: self._natural_sort_key(x))

        return sql_files

    def _extract_script_number(self, filename: str) -> Optional[int]:
        """Extract script number from filename."""
        # Match patterns like "41-UPDATE..." or "41_UPDATE..."
        match = re.match(r"^(\d+)[-_]", filename)
        if match:
            return int(match.group(1))
        return None

    def _natural_sort_key(self, text: str):
        """Generate sort key for natural sorting."""

        def atoi(text):
            return int(text) if text.isdigit() else text

        return [atoi(c) for c in re.split(r"(\d+)", text)]

    def _get_latest_scripts(self, scripts: List[str], count: int) -> List[str]:
        """Get the latest N scripts from the list."""
        if not scripts:
            return []

        # Sort by script number if available, otherwise by name
        scripts_with_numbers = []
        scripts_without_numbers = []

        for script in scripts:
            script_num = self._extract_script_number(script)
            if script_num is not None:
                scripts_with_numbers.append((script_num, script))
            else:
                scripts_without_numbers.append(script)

        # Sort numbered scripts by number
        scripts_with_numbers.sort(key=lambda x: x[0])
        numbered_scripts = [script for _, script in scripts_with_numbers]

        # Combine and take the latest
        all_scripts = numbered_scripts + scripts_without_numbers
        return all_scripts[-count:] if len(all_scripts) > count else all_scripts

    def get_project_status(self, project_name: str) -> Dict:
        """
        Get detailed status for a specific project.

        Args:
            project_name: Name of the project

        Returns:
            Dict with detailed project status
        """
        scan_result = self.scan_project_repository(project_name)

        if not scan_result["available"]:
            return scan_result

        scripts = scan_result["scripts"]

        # Analyze scripts
        script_analysis = {
            "total_scripts": len(scripts),
            "setup_scripts": [
                s for s in scripts if "SETUP" in s.upper() or "CREATE" in s.upper()
            ],
            "update_scripts": [s for s in scripts if "UPDATE" in s.upper()],
            "migration_scripts": [s for s in scripts if "MIGRATION" in s.upper()],
            "gpsub_tickets": [],
        }

        # Extract GPSUB tickets
        for script in scripts:
            match = re.search(r"gpsub-(\d+)", script, re.IGNORECASE)
            if match:
                script_analysis["gpsub_tickets"].append(match.group(1))

        # Remove duplicates from GPSUB tickets
        script_analysis["gpsub_tickets"] = list(set(script_analysis["gpsub_tickets"]))
        script_analysis["gpsub_tickets"].sort()

        scan_result["analysis"] = script_analysis

        return scan_result
