"""
Database Tracker
Handles database connections and script execution tracking.
"""

import psycopg2
from typing import Dict, List, Optional
from pathlib import Path


class DatabaseTracker:
    def __init__(self, config: Dict):
        self.config = config
        self.db_config = {
            "TST": {
                "host": "bdpgsqldev02.petrobras.com.br",
                "port": 5432,
                "database": "SBWBD",
                "user": "USBWBD",
            },
            "HMG": {
                "host": "bdpgsqlhmg01.petrobras.com.br",
                "port": 5432,
                "database": "SBWBH",
                "user": "USBWBH",
            },
            "PRD": {
                "host": "bdpgsqlprd03.petrobras.com.br",
                "port": 5432,
                "database": "SBWBP",
                "user": "USBWBP",
            },
        }

    def setup_tracking_schema(self, environment: str):
        """
        Set up the tracking table and views in the database.

        Args:
            environment: Environment name (TST, HMG, PRD)
        """
        if not self.config["database_tracking"]["enabled"]:
            raise ValueError("Database tracking is disabled in configuration")

        table_name = self.config["database_tracking"]["table_name"]
        view_name = self.config["database_tracking"]["view_name"]

        schema_sql = f"""
-- Create tracking table
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    pi_number VARCHAR(50) NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    script_name VARCHAR(255) NOT NULL,
    execution_date TIMESTAMP DEFAULT NOW(),
    completion_date TIMESTAMP,
    environment VARCHAR(10) DEFAULT CURRENT_SETTING('application_name', true),
    status VARCHAR(50) DEFAULT 'PENDING',
    executed_by VARCHAR(100) DEFAULT CURRENT_USER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_script_log_pi_project 
ON {table_name}(pi_number, project_name);

CREATE INDEX IF NOT EXISTS idx_script_log_status 
ON {table_name}(status, execution_date);

CREATE INDEX IF NOT EXISTS idx_script_log_environment 
ON {table_name}(environment);

-- Create view for easy querying
CREATE OR REPLACE VIEW {view_name} AS
SELECT 
    pi_number,
    project_name,
    script_name,
    status,
    execution_date,
    completion_date,
    environment,
    executed_by,
    notes,
    CASE 
        WHEN status = 'COMPLETED' THEN '✅'
        WHEN status LIKE 'SCRIPT_%_COMPLETED' THEN '⏳'
        WHEN status = 'STARTED' THEN '🔄'
        ELSE '❓'
    END as status_icon
FROM {table_name}
ORDER BY execution_date DESC;

-- Grant permissions (adjust as needed)
-- GRANT SELECT, INSERT, UPDATE ON {table_name} TO your_user;
-- GRANT SELECT ON {view_name} TO your_user;
"""

        try:
            with self._get_connection(environment) as conn:
                with conn.cursor() as cur:
                    cur.execute(schema_sql)
                    conn.commit()
        except Exception as e:
            raise Exception(
                f"Failed to setup tracking schema in {environment}: {str(e)}"
            )

    def get_execution_status(self, environment: str) -> List[Dict]:
        """
        Get script execution status from the database.

        Args:
            environment: Environment name (TST, HMG, PRD)

        Returns:
            List of execution records
        """
        if not self.config["database_tracking"]["enabled"]:
            return []

        view_name = self.config["database_tracking"]["view_name"]

        query = f"""
        SELECT 
            pi_number,
            project_name,
            script_name,
            status,
            execution_date,
            completion_date,
            environment,
            executed_by,
            notes
        FROM {view_name}
        WHERE environment = %s OR environment LIKE %s
        ORDER BY execution_date DESC
        LIMIT 50
        """

        try:
            with self._get_connection(environment) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (environment, f"%{environment}%"))
                    rows = cur.fetchall()

                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            raise Exception(
                f"Failed to get execution status from {environment}: {str(e)}"
            )

    def check_script_status(
        self, environment: str, pi: str, project: str, script: str
    ) -> Optional[Dict]:
        """
        Check if a specific script has been executed.

        Args:
            environment: Environment name
            pi: PI number
            project: Project name
            script: Script name

        Returns:
            Dict with script status or None if not found
        """
        if not self.config["database_tracking"]["enabled"]:
            return None

        table_name = self.config["database_tracking"]["table_name"]

        query = f"""
        SELECT 
            status,
            execution_date,
            completion_date,
            executed_by,
            notes
        FROM {table_name}
        WHERE pi_number = %s 
          AND project_name = %s 
          AND script_name LIKE %s
          AND (environment = %s OR environment LIKE %s)
        ORDER BY execution_date DESC
        LIMIT 1
        """

        try:
            with self._get_connection(environment) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        query,
                        (pi, project, f"%{script}%", environment, f"%{environment}%"),
                    )
                    row = cur.fetchone()

                    if row:
                        columns = [desc[0] for desc in cur.description]
                        return dict(zip(columns, row))
                    return None

        except Exception as e:
            raise Exception(f"Failed to check script status in {environment}: {str(e)}")

    def get_last_executed_script(
        self, environment: str, pi: str, project: str
    ) -> Optional[Dict]:
        """
        Get the last executed script for a project/PI combination.

        Args:
            environment: Environment name
            pi: PI number
            project: Project name

        Returns:
            Dict with last executed script info or None
        """
        if not self.config["database_tracking"]["enabled"]:
            return None

        table_name = self.config["database_tracking"]["table_name"]

        query = f"""
        SELECT 
            script_name,
            status,
            execution_date,
            completion_date,
            executed_by
        FROM {table_name}
        WHERE pi_number = %s 
          AND project_name = %s 
          AND (environment = %s OR environment LIKE %s)
          AND status = 'COMPLETED'
        ORDER BY completion_date DESC
        LIMIT 1
        """

        try:
            with self._get_connection(environment) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (pi, project, environment, f"%{environment}%"))
                    row = cur.fetchone()

                    if row:
                        columns = [desc[0] for desc in cur.description]
                        return dict(zip(columns, row))
                    return None

        except Exception as e:
            raise Exception(
                f"Failed to get last executed script from {environment}: {str(e)}"
            )

    def get_deployment_summary(self, pi: str) -> Dict:
        """
        Get deployment summary for a PI across all environments.

        Args:
            pi: PI number

        Returns:
            Dict with deployment summary
        """
        summary = {}

        for env in self.config["environments"]:
            try:
                env_status = self.get_execution_status(env)
                pi_scripts = [s for s in env_status if s["pi_number"] == pi]

                summary[env] = {
                    "total_executions": len(pi_scripts),
                    "completed": len(
                        [s for s in pi_scripts if s["status"] == "COMPLETED"]
                    ),
                    "in_progress": len(
                        [s for s in pi_scripts if "STARTED" in s["status"]]
                    ),
                    "failed": len(
                        [
                            s
                            for s in pi_scripts
                            if "ERROR" in s["status"] or "FAILED" in s["status"]
                        ]
                    ),
                    "last_execution": pi_scripts[0]["execution_date"]
                    if pi_scripts
                    else None,
                }
            except Exception as e:
                summary[env] = {"error": str(e)}

        return summary

    def _get_connection(self, environment: str):
        """Get database connection for the specified environment."""
        if environment not in self.db_config:
            raise ValueError(f"Unknown environment: {environment}")

        db_params = self.db_config[environment]

        # Note: In a real implementation, you would handle password authentication
        # This could be done through:
        # 1. Environment variables
        # 2. Configuration files
        # 3. Credential management systems
        # 4. Interactive prompts

        try:
            # For now, we'll use a placeholder that would need actual credentials
            conn = psycopg2.connect(
                host=db_params["host"],
                port=db_params["port"],
                database=db_params["database"],
                user=db_params["user"],
                # password=password,  # Would need to be provided
                connect_timeout=10,
            )
            return conn
        except Exception as e:
            raise Exception(f"Failed to connect to {environment} database: {str(e)}")

    def generate_tracking_report(self, pi: str = None, project: str = None) -> str:
        """
        Generate a comprehensive tracking report.

        Args:
            pi: PI number (optional filter)
            project: Project name (optional filter)

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("📊 Database Tracking Report")
        report_lines.append("=" * 50)

        if pi:
            report_lines.append(f"PI Filter: {pi}")
        if project:
            report_lines.append(f"Project Filter: {project}")

        report_lines.append("")

        for env in self.config["environments"]:
            try:
                status_records = self.get_execution_status(env)

                # Apply filters
                if pi:
                    status_records = [s for s in status_records if s["pi_number"] == pi]
                if project:
                    status_records = [
                        s for s in status_records if s["project_name"] == project
                    ]

                report_lines.append(f"🗄️  {env} Environment")
                report_lines.append("-" * 30)

                if status_records:
                    for record in status_records[:10]:  # Show top 10
                        status_icon = "✅" if record["status"] == "COMPLETED" else "⏳"
                        report_lines.append(
                            f"{status_icon} {record['pi_number']}/{record['project_name']}"
                        )
                        report_lines.append(f"   Script: {record['script_name']}")
                        report_lines.append(f"   Status: {record['status']}")
                        report_lines.append(f"   Date: {record['execution_date']}")
                        report_lines.append("")
                else:
                    report_lines.append("   No records found")
                    report_lines.append("")

            except Exception as e:
                report_lines.append(f"   Error accessing {env}: {str(e)}")
                report_lines.append("")

        return "\n".join(report_lines)

    def test_connections(self) -> Dict:
        """
        Test database connections to all environments.

        Returns:
            Dict with connection test results
        """
        results = {}

        for env in self.config["environments"]:
            try:
                with self._get_connection(env) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT version()")
                        version = cur.fetchone()[0]
                        results[env] = {
                            "status": "success",
                            "version": version,
                            "host": self.db_config[env]["host"],
                        }
            except Exception as e:
                results[env] = {
                    "status": "error",
                    "error": str(e),
                    "host": self.db_config[env]["host"],
                }

        return results
