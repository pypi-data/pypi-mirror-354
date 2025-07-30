"""
Deployment Checker
Checks deployment status across repositories and generates reports.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from documentation_updater import DocumentationUpdater
from repository_scanner import RepositoryScanner


class DeploymentChecker:
    def __init__(self, config: Dict):
        self.config = config
        self.scripts_repo = (
            Path(config["repositories"]["scripts_repo"]).expanduser().absolute()
        )
        self.doc_updater = DocumentationUpdater(config)
        self.repo_scanner = RepositoryScanner(config)

    def get_pi_status(self, pi: str, check_database: bool = False) -> Dict:
        """
        Get deployment status for all projects in a specific PI.

        Args:
            pi: PI number (e.g., 'gpsub-pi07')
            check_database: Whether to check actual database execution status

        Returns:
            Dict with status for each project and environment
        """
        status = {}

        # Find all projects that have scripts in this PI
        pi_dir = self.scripts_repo / "scripts" / pi / "postgres" / "usbwb"

        if not pi_dir.exists():
            return status

        for project_dir in pi_dir.iterdir():
            if project_dir.is_dir():
                project_name = self._map_script_path_to_project(project_dir.name)
                if project_name:
                    status[project_name] = self._get_project_pi_status(
                        project_name, pi, check_database
                    )

        return status

    def get_project_status(
        self, project_name: str, check_database: bool = False
    ) -> Dict:
        """
        Get deployment status for all PIs of a specific project.

        Args:
            project_name: Name of the project
            check_database: Whether to check actual database execution status

        Returns:
            Dict with status for each PI and environment
        """
        if project_name not in self.config["projects"]:
            raise ValueError(f"Project '{project_name}' not found in configuration")

        project_config = self.config["projects"][project_name]
        script_path = project_config["script_path"]

        status = {}

        # Find all PIs that have scripts for this project
        scripts_dir = self.scripts_repo / "scripts"

        if not scripts_dir.exists():
            return status

        for pi_dir in scripts_dir.iterdir():
            if pi_dir.is_dir() and pi_dir.name.startswith(("gpsub-", "sbwb-", "nvlw-")):
                project_script_dir = pi_dir / "postgres" / "usbwb" / script_path
                if project_script_dir.exists():
                    pi_name = pi_dir.name
                    status[pi_name] = self._get_project_pi_status(
                        project_name, pi_name, check_database
                    )

        return status

    def get_overall_status(self, check_database: bool = False) -> Dict:
        """
        Get deployment status for all projects and PIs.

        Args:
            check_database: Whether to check actual database execution status

        Returns:
            Dict with complete status overview
        """
        status = {}

        for project_name in self.config["projects"].keys():
            try:
                project_status = self.get_project_status(project_name, check_database)
                if project_status:
                    status[project_name] = project_status
            except Exception as e:
                status[project_name] = {"error": str(e)}

        return status

    def generate_deployment_report(
        self, pi: str, target_environment: Optional[str] = None
    ) -> Dict:
        """
        Generate a comprehensive deployment report for a PI.

        Args:
            pi: PI number
            target_environment: Specific environment to target (optional)

        Returns:
            Dict with deployment report
        """
        pi_status = self.get_pi_status(pi)

        report = {
            "pi": pi,
            "target_environment": target_environment,
            "projects": {},
            "summary": {
                "total_projects": 0,
                "ready_projects": 0,
                "pending_projects": 0,
            },
        }

        for project_name, env_status in pi_status.items():
            project_report = {
                "ready": True,
                "scripts": [],
                "missing_environments": [],
                "deployment_order": [],
            }

            # Get scripts for this project/PI
            scripts = self._get_pi_scripts(project_name, pi)
            project_report["scripts"] = scripts

            # Check deployment status for each environment
            environments = (
                [target_environment]
                if target_environment
                else self.config["environments"]
            )

            for env in environments:
                env_data = env_status.get(env, {})
                if not env_data.get("deployed", False):
                    project_report["missing_environments"].append(env)
                    project_report["ready"] = False

            # Determine deployment order
            if target_environment:
                if target_environment in project_report["missing_environments"]:
                    project_report["deployment_order"] = [target_environment]
            else:
                project_report["deployment_order"] = project_report[
                    "missing_environments"
                ]

            report["projects"][project_name] = project_report
            report["summary"]["total_projects"] += 1

            if project_report["ready"]:
                report["summary"]["ready_projects"] += 1
            else:
                report["summary"]["pending_projects"] += 1

        return report

    def _get_project_pi_status(
        self, project_name: str, pi: str, check_database: bool
    ) -> Dict:
        """Get status for a specific project and PI."""
        # Get documentation status
        doc_status = self.doc_updater.get_deployment_status(project_name)

        # Get scripts available in PI folder
        available_scripts = self._get_pi_scripts(project_name, pi)

        status = {}
        for env in self.config["environments"]:
            env_status = {
                "deployed": False,
                "scripts_deployed": [],
                "scripts_pending": [],
                "last_deployment": None,
            }

            # Check each script's deployment status
            for script in available_scripts:
                script_status = doc_status.get(script, {})
                env_deployment = script_status.get(env)

                if env_deployment and env_deployment != "-":
                    env_status["scripts_deployed"].append(script)
                    if (
                        not env_status["last_deployment"]
                        or env_deployment > env_status["last_deployment"]
                    ):
                        env_status["last_deployment"] = env_deployment
                else:
                    env_status["scripts_pending"].append(script)

            # Determine if environment is fully deployed
            env_status["deployed"] = (
                len(env_status["scripts_pending"]) == 0 and len(available_scripts) > 0
            )

            # Add database confirmation if requested
            if check_database:
                env_status["db_confirmed"] = self._check_database_status(
                    project_name, pi, env
                )

            status[env] = env_status

        return status

    def _get_pi_scripts(self, project_name: str, pi: str) -> List[str]:
        """Get all scripts for a project in a specific PI."""
        if project_name not in self.config["projects"]:
            return []

        project_config = self.config["projects"][project_name]
        script_path = project_config["script_path"]

        pi_script_dir = (
            self.scripts_repo / "scripts" / pi / "postgres" / "usbwb" / script_path
        )

        if not pi_script_dir.exists():
            return []

        scripts = []
        for file in pi_script_dir.glob("*.sql"):
            if file.is_file() and not file.name.startswith("."):
                scripts.append(file.name)

        # Sort scripts naturally
        scripts.sort(key=lambda x: self._natural_sort_key(x))

        return scripts

    def _map_script_path_to_project(self, script_path: str) -> Optional[str]:
        """Map script path to project name."""
        for project_name, config in self.config["projects"].items():
            if config["script_path"] == script_path:
                return project_name
        return None

    def _check_database_status(
        self, project_name: str, pi: str, environment: str
    ) -> bool:
        """Check if scripts are actually executed in the database."""
        # This would need to be implemented with actual database connections
        # For now, return False as placeholder
        # In a real implementation, you would:
        # 1. Connect to the database for the given environment
        # 2. Query the script_execution_log table
        # 3. Check if scripts for this project/PI are marked as completed
        return False

    def _natural_sort_key(self, text: str):
        """Generate sort key for natural sorting."""
        import re

        def atoi(text):
            return int(text) if text.isdigit() else text

        return [atoi(c) for c in re.split(r"(\d+)", text)]

    def get_deployment_gaps(self, pi: str) -> Dict:
        """
        Identify deployment gaps - scripts that are deployed in higher environments
        but not in lower ones.

        Args:
            pi: PI number

        Returns:
            Dict with deployment gap analysis
        """
        pi_status = self.get_pi_status(pi)
        gaps = {}

        for project_name, env_status in pi_status.items():
            project_gaps = []

            # Check for gaps: PRD deployed but not HMG, HMG deployed but not TST
            tst_scripts = set(env_status.get("TST", {}).get("scripts_deployed", []))
            hmg_scripts = set(env_status.get("HMG", {}).get("scripts_deployed", []))
            prd_scripts = set(env_status.get("PRD", {}).get("scripts_deployed", []))

            # PRD but not HMG
            prd_not_hmg = prd_scripts - hmg_scripts
            if prd_not_hmg:
                project_gaps.append(
                    {"type": "PRD deployed but not HMG", "scripts": list(prd_not_hmg)}
                )

            # HMG but not TST
            hmg_not_tst = hmg_scripts - tst_scripts
            if hmg_not_tst:
                project_gaps.append(
                    {"type": "HMG deployed but not TST", "scripts": list(hmg_not_tst)}
                )

            if project_gaps:
                gaps[project_name] = project_gaps

        return gaps

    def get_next_deployments(self) -> Dict:
        """
        Get the next recommended deployments across all projects.

        Returns:
            Dict with recommended next deployments
        """
        recommendations = {"TST": [], "HMG": [], "PRD": []}

        overall_status = self.get_overall_status()

        for project_name, pi_status in overall_status.items():
            if "error" in pi_status:
                continue

            for pi, env_status in pi_status.items():
                # Check deployment progression: TST -> HMG -> PRD
                tst_deployed = env_status.get("TST", {}).get("deployed", False)
                hmg_deployed = env_status.get("HMG", {}).get("deployed", False)
                prd_deployed = env_status.get("PRD", {}).get("deployed", False)

                # Recommend TST if not deployed
                if not tst_deployed:
                    recommendations["TST"].append(
                        {
                            "project": project_name,
                            "pi": pi,
                            "scripts": env_status.get("TST", {}).get(
                                "scripts_pending", []
                            ),
                        }
                    )

                # Recommend HMG if TST is deployed but HMG is not
                elif tst_deployed and not hmg_deployed:
                    recommendations["HMG"].append(
                        {
                            "project": project_name,
                            "pi": pi,
                            "scripts": env_status.get("HMG", {}).get(
                                "scripts_pending", []
                            ),
                        }
                    )

                # Recommend PRD if HMG is deployed but PRD is not
                elif hmg_deployed and not prd_deployed:
                    recommendations["PRD"].append(
                        {
                            "project": project_name,
                            "pi": pi,
                            "scripts": env_status.get("PRD", {}).get(
                                "scripts_pending", []
                            ),
                        }
                    )

        return recommendations
