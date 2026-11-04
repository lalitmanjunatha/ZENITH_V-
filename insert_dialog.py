#!/usr/bin/env python3
"""Insert Project Companion dialog code into zenith_gui.py"""

import sys

with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

# Find the line index where _ReconnectSignal starts (line 452 -> index 451)
reconnect_idx = -1
for i in range(len(lines)):
    if '_ReconnectSignal' in lines[i] and 'class _ReconnectSignal' in lines[i]:
        reconnect_idx = i
        break

if reconnect_idx == -1:
    print('ERROR: Could not find _ReconnectSignal class')
    sys.exit(1)

print(f'Found _ReconnectSignal at line {reconnect_idx+1}')

# Project Companion dialog code to insert
dialog_code = '''    def open_project_companion(self):
        """Open the Project Companion dialog."""
        if hasattr(self, '_pc_dialog') and self._pc_dialog is not None:
            self._pc_dialog._pc_refresh_projects()
            self.zenith_live.ui.write_log("SYS: Project Companion dialog reopened")
        else:
            self._pc_dialog = ProjectCompanionDialog(self)
            self.zenith_live.ui.write_log("SYS: Project Companion dialog opened")

    def close_project_companion(self):
        """Close the Project Companion dialog."""
        if hasattr(self, '_pc_dialog') and self._pc_dialog is not None:
            self._pc_dialog = None
            self.zenith_live.ui.write_log("SYS: Project Companion dialog closed")

    def _pc_refresh_projects(self):
        """Refresh the project list from the service."""
        try:
            result = get_pc_service().project_list()
            if result.get("ok"):
                self._pc_projects = result.get("projects", [])
                self._pc_update_project_list_display()
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to list projects: {result.get('error', 'unknown')}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error listing projects: {str(e)}"
            )

    def _pc_update_project_list_display(self):
        """Update the visual project list display."""
        project_count = len(self._pc_projects) if hasattr(self, '_pc_projects') else 0
        if project_count == 0:
            self.zenith_live.ui.write_log(
                "SYS: No projects found. Use 'Create Project' to start a new project."
            )
        else:
            project_names = [p.get('name', 'Unknown') for p in self._pc_projects]
            self.zenith_live.ui.write_log(
                f"SYS: Found {project_count} project{'s' if project_count > 1 else ''}: "
                + ", ".join(project_names)
            )

    def _pc_create_project(self, name, description, project_type, problem_statement="",
                         goals=None, acceptance_criteria=None, constraints=None):
        """Create a new project through the service."""
        try:
            result = get_pc_service().project_create(
                name, description, project_type, problem_statement,
                goals or [], acceptance_criteria or [], constraints or []
            )
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Project '{name}' created successfully (ID: {result.get('project_id')})"
                )
                self._pc_refresh_projects()
                return True
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to create project: {result.get('error', 'unknown')}"
                )
                return False
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error creating project: {str(e)}"
            )
            return False

    def _pc_select_project(self, project_id):
        """Select a project and show its details."""
        self._pc_current_project_id = project_id
        project = next((p for p in self._pc_projects if p.get('id') == project_id), None)
        if project:
            self.zenith_live.ui.write_log(
                f"SYS: Showing details for project '{project.get('name', 'Unknown')}'"
            )
            self._pc_show_project_details(project)
        else:
            self.zenith_live.ui.write_log(
                "SYS: Project not found in current list"
            )

    def _pc_show_project_details(self, project):
        """Show project details in the UI."""
        details = [
            f"Project: {project.get('name', 'Unknown')}",
            f"Type: {project.get('project_type', 'unknown')}",
            f"ID: {project.get('id', 'unknown')}",
        ]
        if project.get('description'):
            details.append(f"Description: {project.get('description')}")
        if project.get('stage'):
            details.append(f"Stage: {project.get('stage')}")
        self.zenith_live.ui.write_log("SYS: Project Details:")
        for detail in details:
            self.zenith_live.ui.write_log(f"  {detail}")

    def _pc_add_task(self, project_id, name, description, stage, dependencies=None):
        """Add a task to a project."""
        try:
            result = get_pc_service().project_add_task(
                project_id, name, description, stage, dependencies or []
            )
            if result.get('ok'):
                self.zenith_live.ui.write_log(
                    f"SYS: Task '{name}' added successfully (ID: {result.get('task_id')})"
                )
                self._pc_refresh_projects()
                return True
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to add task: {result.get('error', 'unknown')}"
                )
                return False
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error adding task: {str(e)}"
            )
            return False

    def _pc_update_task_status(self, project_id, task_id, status, result="", test_results=None):
        """Update a task's status."""
        try:
            result = get_pc_service().project_update_task_status(
                project_id, task_id, status, result, test_results or []
            )
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Task '{task_id}' status updated to {status}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error updating task status: {str(e)}"
            )

    def _pc_save_checkpoint(self, project_id, label):
        """Save a project checkpoint."""
        try:
            result = get_pc_service().project_save_checkpoint(project_id, label)
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Checkpoint '{label}' saved successfully for project {project_id}"
                )
                self._pc_refresh_projects()
                return True
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to save checkpoint: {result.get('error', 'unknown')}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error saving checkpoint: {str(e)}"
            )
        return False

    def _pc_list_checkpoints(self, project_id):
        """List checkpoints for a project."""
        self.zenith_live.ui.write_log(
            "SYS: Checkpoint listing: use 'Save Checkpoint' to create one."
        )

class ProjectCompanionDialog:
    """Compact Project Companion view for ZENITH VADRYK Edition."""
    def __init__(self, zenith_live):
        self.zenith_live = zenith_live
        self.zenith_live._pc_dialog = self
        self.current_project_id = None
        self._pc_projects = []
        self._pc_current_project_id = None
        self.zenith_live.ui.set_state("LISTENING")
        self.zenith_live.ui.write_log("SYS: Opening Project Companion...")
        self._pc_refresh_projects()

    def _pc_refresh_projects(self):
        """Refresh the project list from the service."""
        try:
            result = get_pc_service().project_list()
            if result.get("ok"):
                self._pc_projects = result.get("projects", [])
                self._pc_update_project_list_display()
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to list projects: {result.get('error', 'unknown')}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error listing projects: {str(e)}"
            )

    def _pc_update_project_list_display(self):
        """Update the visual project list display."""
        project_count = len(self._pc_projects)
        if project_count == 0:
            self.zenith_live.ui.write_log(
                "SYS: No projects found. Use 'Create Project' to start a new project."
            )
        else:
            project_names = [p.get('name', 'Unknown') for p in self._pc_projects]
            self.zenith_live.ui.write_log(
                f"SYS: Found {project_count} project{'s' if project_count > 1 else ''}: "
                + ", ".join(project_names)
            )

    def _pc_create_project(self, name, description, project_type, problem_statement="",
                         goals=None, acceptance_criteria=None, constraints=None):
        """Create a new project through the service."""
        try:
            result = get_pc_service().project_create(
                name, description, project_type, problem_statement,
                goals or [], acceptance_criteria or [], constraints or []
            )
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Project '{name}' created successfully (ID: {result.get('project_id')})"
                )
                self._pc_refresh_projects()
                return True
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to create project: {result.get('error', 'unknown')}"
                )
            return False
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error creating project: {str(e)}"
            )
            return False

    def _pc_select_project(self, project_id):
        """Select a project and show its details."""
        self._pc_current_project_id = project_id
        project = next((p for p in self._pc_projects if p.get('id') == project_id), None)
        if project:
            self.zenith_live.ui.write_log(
                f"SYS: Showing details for project '{project.get('name', 'Unknown')}'"
            )
            self._pc_show_project_details(project)
        else:
            self.zenith_live.ui.write_log(
                "SYS: Project not found in current list"
            )

    def _pc_show_project_details(self, project):
        """Show project details in the UI."""
        details = [
            f"Project: {project.get('name', 'Unknown')}",
            f"Type: {project.get('project_type', 'unknown')}",
            f"ID: {project.get('id', 'unknown')}",
        ]
        if project.get('description'):
            details.append(f"Description: {project.get('description')}")
        if project.get('stage'):
            details.append(f"Stage: {project.get('stage')}")
        self.zenith_live.ui.write_log("SYS: Project Details:")
        for detail in details:
            self.zenith_live.ui.write_log(f"  {detail}")

    def _pc_add_task(self, project_id, name, description, stage, dependencies=None):
        """Add a task to a project."""
        try:
            result = get_pc_service().project_add_task(
                project_id, name, description, stage, dependencies or []
            )
            if result.get('ok'):
                self.zenith_live.ui.write_log(
                    f"SYS: Task '{name}' added successfully (ID: {result.get('task_id')})"
                )
                self._pc_refresh_projects()
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error adding task: {str(e)}"
            )

    def _pc_update_task_status(self, project_id, task_id, status, result="", test_results=None):
        """Update a task's status."""
        try:
            result = get_pc_service().project_update_task_status(
                project_id, task_id, status, result, test_results or []
            )
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Task '{task_id}' status updated to {status}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error updating task status: {str(e)}"
            )

    def _pc_save_checkpoint(self, project_id, label):
        """Save a project checkpoint."""
        try:
            result = get_pc_service().project_save_checkpoint(project_id, label)
            if result.get("ok"):
                self.zenith_live.ui.write_log(
                    f"SYS: Checkpoint '{label}' saved successfully for project {project_id}"
                )
            else:
                self.zenith_live.ui.write_log(
                    f"SYS: Failed to save checkpoint: {result.get('error', 'unknown')}"
                )
        except Exception as e:
            self.zenith_live.ui.write_log(
                f"SYS: Error saving checkpoint: {str(e)}"
            )

    def _pc_list_checkpoints(self, project_id):
        """List checkpoints for a project."""
        self.zenith_live.ui.write_log(
            "SYS: Checkpoint listing: use 'Save Checkpoint' to create one."
        )
'''

# Insert the dialog code before _ReconnectSignal
new_lines = lines[:reconnect_idx] + [dialog_code] + lines[reconnect_idx:]

with open('zenith_gui.py', 'w', errors='replace') as f:
    f.writelines(new_lines)

print(f'Project Companion dialog code inserted at line {reconnect_idx+1}')
print(f'Total lines after insertion: {len(new_lines)}')