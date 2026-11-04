#!/usr/bin/env python
import re

with open('zenith_gui.py', encoding='utf-8') as f:
    content = f.read()

# Find the TOOL_DECLARATIONS closing bracket
# Search for the pattern: the last ']' that closes TOOL_DECLARATIONS
# We'll find it by looking for the pattern after the presentation/simulation/webcam tool blocks

# Alternative approach: just append the new tools at the end of TOOL_DECLARATIONS
# by finding where the list ends

# Let's just append after we find the TOOL_DECLARATIONS section
# Find the line with "]" that closes TOOL_DECLARATIONS
lines = content.split('\n')
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'TOOL_DECLARATIONS = [' in line:
        start_idx = i
    if start_idx is not None and '{' in line and 'TOOL_DECLARATIONS' not in line:
        # Count braces to find the end
        pass

# Simpler approach: just locate the closing bracket of TOOL_DECLARATIONS
# The TOOL_DECLARATIONS list ends with a ']' followed by some blank lines and then other code
# Let's find it by looking for the pattern

# Actually, let me just append the new tools by finding a good insertion point
# I'll look for the line after "fun_fact, compliment, joke, motivation," which is near the end

# Let me just use a simpler approach - find the end of the file and insert before any remaining code
# Or better, let me just append to the TOOL_DECLARATIONS by replacing the closing bracket line

# Find the line number of the closing bracket
close_line = None
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == ']' and i > 350:  # TOOL_DECLARATIONS is around line 171+
        close_line = i
        break

print(f'Closing bracket at line: {close_line}')

if close_line is not None:
    # Insert the new tools before this line
    new_tools = """
    # ── Project Companion ──────────────────────────────────────────────
    {
        "name": "_pc_project_create",
        "description": "Create a new project with name, description, type, and optional problem statement, goals, acceptance criteria, and constraints.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "name": {"type": "STRING", "description": "Project name"},
                "description": {"type": "STRING", "description": "Project description"},
                "project_type": {"type": "STRING", "description": "Project type (software, hardware)"},
                "problem_statement": {"type": "STRING", "description": "What problem does this project solve?"},
                "goals": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Project goals"},
                "acceptance_criteria": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Acceptance criteria"},
                "constraints": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Project constraints"}
            },
            "required": ["name", "description", "project_type"]
        }
    },
    {
        "name": "_pc_project_list",
        "description": "List all existing projects.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "_pc_project_state_summary",
        "description": "Get a project's state summary including task counts, stage, and next recommended action.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "project_id": {"type": "STRING", "description": "Project ID to look up"}
            },
            "required": ["project_id"]
        }
    },
    {
        "name": "_pc_project_add_task",
        "description": "Add a task to a project.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "project_id": {"type": "STRING", "description": "Project ID"},
                "name": {"type": "STRING", "description": "Task name"},
                "description": {"type": "STRING", "description": "Task description"},
                "stage": {"type": "STRING", "description": "Project stage (ideation, planning, building, testing, verifying, completed)"},
                "dependencies": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "Task dependencies"}
            },
            "required": ["project_id", "name", "description", "stage"]
        }
    },
    {
        "name": "_pc_project_update_task_status",
        "description": "Update a task's status and optionally record test results.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "project_id": {"type": "STRING", "description": "Project ID"},
                "task_id": {"type": "STRING", "description": "Task ID"},
                "status": {"type": "STRING", "description": "Task status (pending, in_progress, verified, completed, blocked)"},
                "result": {"type": "STRING", "description": "Test result description"},
                "test_results": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "List of test result strings"}
            },
            "required": ["project_id", "task_id", "status"]
        }
    },
    {
        "name": "_pc_project_save_checkpoint",
        "description": "Save a project checkpoint with a label.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "project_id": {"type": "STRING", "description": "Project ID"},
                "label": {"type": "STRING", "description": "Checkpoint label/name"}
            },
            "required": ["project_id", "label"]
        }
    },
]

# Insert the new tools before the closing bracket
# Replace the closing ']' with the new tools + closing ']'
old_closing = lines[close_line]
new_closing = new_tools + '\n]'
lines[close_line] = new_closing

# Also need to handle the line after the closing bracket
# Check if there's content after the closing bracket
after_content = '\n'.join(lines[close_line+1:])
# Remove the old closing bracket and add the new one
# Actually, we need to be more careful

# Let me just rewrite the whole thing more carefully
print(f'Found closing bracket at line {close_line+1}')
else:
    print('Closing bracket not found')
"