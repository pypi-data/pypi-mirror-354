"""
Script Consolidator
Handles consolidating database scripts from individual repositories into
the centralized sbwb-db-scripts repository with transaction wrapping and tracking.
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import shutil


class ScriptConsolidator:
    def __init__(self, config: Dict):
        self.config = config
        self.scripts_repo = (
            Path(config["repositories"]["scripts_repo"]).expanduser().absolute()
        )

    def consolidate_scripts(
        self,
        project: str,
        pi: str,
        from_script: Optional[int] = None,
        to_script: Optional[int] = None,
        dry_run: bool = False,
    ) -> Dict:
        """
        Consolidate scripts from source repository to sbwb-db-scripts.

        Args:
            project: Project name (e.g., 'sbwb-basicdata-supplies')
            pi: PI number (e.g., 'gpsub-pi07')
            from_script: Starting script number (optional)
            to_script: Ending script number (optional)
            dry_run: If True, only show what would be done

        Returns:
            Dict with consolidation results
        """
        project_config = self.config["projects"][project]
        source_repo = Path(project_config["source_repo"]).expanduser().absolute()
        source_path = source_repo / project_config["source_path"]

        if not source_path.exists():
            raise FileNotFoundError(f"Source path not found: {source_path}")

        # Find scripts to consolidate
        scripts_to_consolidate = self._find_scripts_in_range(
            source_path, from_script, to_script
        )

        if not scripts_to_consolidate:
            raise ValueError("No scripts found in the specified range")

        # Generate output path
        script_path = project_config["script_path"]
        output_dir = (
            self.scripts_repo / "scripts" / pi / "postgres" / "usbwb" / script_path
        )

        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)

        # Generate consolidated script
        consolidated_content = self._generate_consolidated_script(
            scripts_to_consolidate, source_path, project, pi
        )

        # Determine output filename
        if from_script and to_script:
            output_filename = f"{from_script:02d}-{to_script:02d}-CONSOLIDATED.sql"
        else:
            script_numbers = [
                self._extract_script_number(s) for s in scripts_to_consolidate
            ]
            script_numbers = [n for n in script_numbers if n is not None]
            if script_numbers:
                min_num, max_num = min(script_numbers), max(script_numbers)
                output_filename = f"{min_num:02d}-{max_num:02d}-CONSOLIDATED.sql"
            else:
                output_filename = (
                    f"CONSOLIDATED-{datetime.now().strftime('%Y%m%d')}.sql"
                )

        output_path = output_dir / output_filename

        if not dry_run:
            # Write consolidated script
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(consolidated_content)

            # Copy individual scripts too
            for script in scripts_to_consolidate:
                source_file = source_path / script
                dest_file = output_dir / script
                if source_file.exists():
                    shutil.copy2(source_file, dest_file)

            # Generate README
            self._generate_readme(output_dir, scripts_to_consolidate, pi)

        return {
            "output_path": str(output_path),
            "scripts": scripts_to_consolidate,
            "project": project,
            "pi": pi,
        }

    def create_deployment_package(
        self, pi: str, environment: str, output_dir: Optional[str] = None
    ) -> str:
        """
        Create a deployment package for a specific PI and environment.

        Args:
            pi: PI number
            environment: Target environment (TST, HMG, PRD)
            output_dir: Output directory (optional)

        Returns:
            Path to the created package
        """
        if output_dir is None:
            output_dir = f"deployment-packages"

        package_dir = (
            Path(output_dir) / f"{pi}-{environment}-{datetime.now().strftime('%Y%m%d')}"
        )
        package_dir.mkdir(parents=True, exist_ok=True)

        # Find all scripts for this PI
        pi_dir = self.scripts_repo / "scripts" / pi / "postgres" / "usbwb"

        if not pi_dir.exists():
            raise FileNotFoundError(f"PI directory not found: {pi_dir}")

        # Copy all project scripts
        for project_dir in pi_dir.iterdir():
            if project_dir.is_dir():
                for sql_file in project_dir.glob("*.sql"):
                    dest_file = package_dir / f"{project_dir.name}_{sql_file.name}"
                    shutil.copy2(sql_file, dest_file)

        # Generate deployment script
        deployment_script = self._generate_deployment_script(
            package_dir, pi, environment
        )

        with open(package_dir / "deploy.sql", "w", encoding="utf-8") as f:
            f.write(deployment_script)

        return str(package_dir)

    def _find_scripts_in_range(
        self, source_path: Path, from_script: Optional[int], to_script: Optional[int]
    ) -> List[str]:
        """Find SQL scripts in the specified range."""
        if not source_path.exists():
            return []

        sql_files = []
        for file in source_path.glob("*.sql"):
            if file.name.lower().endswith(".sql"):
                sql_files.append(file.name)

        # Sort files naturally
        sql_files.sort(key=lambda x: self._natural_sort_key(x))

        if from_script is not None or to_script is not None:
            filtered_files = []
            for file in sql_files:
                script_num = self._extract_script_number(file)
                if script_num is not None:
                    if from_script is not None and script_num < from_script:
                        continue
                    if to_script is not None and script_num > to_script:
                        continue
                    filtered_files.append(file)
            return filtered_files

        return sql_files

    def _extract_script_number(self, filename: str) -> Optional[int]:
        """Extract script number from filename."""
        # Match patterns like "41-UPDATE..." or "41_UPDATE..."
        match = re.match(r"^(\d+)[-_]", filename)
        if match:
            return int(match.group(1))
        return None

    def _natural_sort_key(self, text: str) -> Tuple:
        """Generate sort key for natural sorting."""

        def atoi(text):
            return int(text) if text.isdigit() else text

        return [atoi(c) for c in re.split(r"(\d+)", text)]

    def _generate_consolidated_script(
        self, scripts: List[str], source_path: Path, project: str, pi: str
    ) -> str:
        """Generate consolidated script with transaction wrapping and tracking."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract GPSUB tickets from script names
        gpsub_tickets = []
        for script in scripts:
            match = re.search(r"gpsub-(\d+)", script, re.IGNORECASE)
            if match:
                gpsub_tickets.append(match.group(1))

        script_range = (
            f"{scripts[0]} to {scripts[-1]}" if len(scripts) > 1 else scripts[0]
        )

        header = f"""-- ============================================================================
-- CONSOLIDATED DATABASE SCRIPT
-- ============================================================================
-- Generated by: dbmanager-cli
-- Generated on: {timestamp}
-- PI: {pi}
-- Project: {project}
-- Scripts: {script_range}
-- GPSUB Tickets: {', '.join(gpsub_tickets) if gpsub_tickets else 'N/A'}
-- ============================================================================

-- Set application name for tracking
SET application_name = '{pi}_{project}';

BEGIN;

-- Create tracking table if it doesn't exist
CREATE TABLE IF NOT EXISTS script_execution_log (
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

-- Create index if it doesn't exist
CREATE INDEX IF NOT EXISTS idx_script_log_pi_project 
ON script_execution_log(pi_number, project_name);

-- Insert initial tracking record
INSERT INTO script_execution_log (
    pi_number, 
    project_name, 
    script_name, 
    execution_date, 
    environment,
    status,
    notes
) VALUES (
    '{pi}', 
    '{project}', 
    'CONSOLIDATED_{len(scripts)}_SCRIPTS', 
    NOW(), 
    CURRENT_SETTING('application_name', true),
    'STARTED',
    'Consolidated script containing: {", ".join(scripts)}'
);

-- Get the tracking record ID for updates
DO $$
DECLARE
    tracking_id INTEGER;
BEGIN
    SELECT id INTO tracking_id 
    FROM script_execution_log 
    WHERE pi_number = '{pi}' 
      AND project_name = '{project}' 
      AND script_name = 'CONSOLIDATED_{len(scripts)}_SCRIPTS'
      AND status = 'STARTED'
    ORDER BY execution_date DESC 
    LIMIT 1;
    
    -- Store in a temp table for later reference
    CREATE TEMP TABLE IF NOT EXISTS current_tracking (id INTEGER);
    DELETE FROM current_tracking;
    INSERT INTO current_tracking VALUES (tracking_id);
END $$;

"""

        # Add individual scripts
        content_parts = [header]

        for i, script in enumerate(scripts, 1):
            script_file = source_path / script

            # Extract GPSUB ticket from filename
            gpsub_match = re.search(r"gpsub-(\d+)", script, re.IGNORECASE)
            gpsub_ticket = gpsub_match.group(1) if gpsub_match else "N/A"

            script_header = f"""
-- ============================================================================
-- Script {i}/{len(scripts)}: {script}
-- GPSUB Ticket: {gpsub_ticket}
-- ============================================================================

"""
            content_parts.append(script_header)

            # Read and add script content
            if script_file.exists():
                with open(script_file, "r", encoding="utf-8") as f:
                    script_content = f.read().strip()
                    content_parts.append(script_content)
            else:
                content_parts.append(f"-- ERROR: Script file not found: {script}")

            # Add tracking update
            tracking_update = f"""

-- Update tracking for script {i}
UPDATE script_execution_log 
SET status = 'SCRIPT_{i}_COMPLETED',
    notes = notes || ' | Script {i} ({script}) completed at ' || NOW()::TEXT
WHERE id = (SELECT id FROM current_tracking);

"""
            content_parts.append(tracking_update)

        # Add footer with final tracking update
        footer = f"""
-- ============================================================================
-- CONSOLIDATION COMPLETE
-- ============================================================================

-- Final tracking update
UPDATE script_execution_log 
SET status = 'COMPLETED', 
    completion_date = NOW(),
    notes = notes || ' | All scripts completed successfully at ' || NOW()::TEXT
WHERE id = (SELECT id FROM current_tracking);

-- Clean up temp table
DROP TABLE IF EXISTS current_tracking;

COMMIT;

-- ============================================================================
-- END OF CONSOLIDATED SCRIPT
-- ============================================================================
"""

        content_parts.append(footer)

        return "\n".join(content_parts)

    def _generate_deployment_script(
        self, package_dir: Path, pi: str, environment: str
    ) -> str:
        """Generate deployment script for the package."""
        sql_files = list(package_dir.glob("*.sql"))
        sql_files = [f for f in sql_files if f.name != "deploy.sql"]
        sql_files.sort()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        deployment_script = f"""-- ============================================================================
-- DEPLOYMENT SCRIPT
-- ============================================================================
-- Generated by: dbmanager-cli
-- Generated on: {timestamp}
-- PI: {pi}
-- Environment: {environment}
-- ============================================================================

-- Execute in order:
"""

        for i, sql_file in enumerate(sql_files, 1):
            deployment_script += f"""
-- {i}. Execute: {sql_file.name}
-- \\i {sql_file.name}
"""

        deployment_script += """
-- ============================================================================
-- DEPLOYMENT COMPLETE
-- ============================================================================
"""

        return deployment_script

    def _generate_readme(self, output_dir: Path, scripts: List[str], pi: str):
        """Generate README file for the consolidated scripts."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        readme_content = f"""# Database Scripts - {pi}

Generated on: {timestamp}

## Instructions

Execute these scripts in the PostgreSQL database `SBWB` using the appropriate user.

### Scripts in order:

"""

        for i, script in enumerate(scripts, 1):
            gpsub_match = re.search(r"gpsub-(\d+)", script, re.IGNORECASE)
            gpsub_ticket = gpsub_match.group(1) if gpsub_match else "N/A"
            readme_content += f"{i}. [{script}]({script}) (GPSUB-{gpsub_ticket})\n"

        readme_content += f"""
### Consolidated Script

A consolidated version with transaction wrapping and tracking is available:
- Look for files with "CONSOLIDATED" in the name

### Database Connection Information

|         |              TST              |              HMG              |              PRD              |
| ------: | :---------------------------: | :---------------------------: | :---------------------------: |
|    Host | bdpgsqldev02.petrobras.com.br | bdpgsqlhmg01.petrobras.com.br | bdpgsqlprd03.petrobras.com.br |
|   Porta |             5432              |             5432              |             5432              |
|   Banco |             SBWBD             |             SBWBH             |             SBWBP             |
| Usuário |            USBWBD             |            USBWBH             |            USBWBP             |

### Tracking

These scripts include database tracking. After execution, you can check status with:

```sql
SELECT * FROM script_execution_log 
WHERE pi_number = '{pi}' 
ORDER BY execution_date DESC;
```
"""

        readme_path = output_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
