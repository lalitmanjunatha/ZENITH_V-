path = 'zenith_gui.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('TOOL_DECLARATIONS')
if start == -1:
    print('NOT FOUND')
    raise SystemExit
bracket = content.find('[', start)
count = 0
i = bracket
end = -1
while i < len(content):
    if content[i] == '[':
        count += 1
    elif content[i] == ']':
        count -= 1
        if count == 0:
            end = i
            break
    i += 1

pc_decls = [
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_create",
                "description": "Create a new Project Companion project with name, description, type, problem statement, goals, acceptance criteria, and constraints.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "project_type": {"type": "string"},
                        "problem_statement": {"type": "string"},
                        "goals": {"type": "array", "items": {"type": "string"}},
                        "acceptance_criteria": {"type": "array", "items": {"type": "string"}},
                        "constraints": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["name", "description", "project_type"],
                },
            },
        },
''',
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_list",
                "description": "List all Project Companion projects.",
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
''',
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_state_summary",
                "description": "Get Project Companion state summary for a project.",
                "parameters": {
                    "type": "object",
                    "properties": {"project_id": {"type": "string"}},
                    "required": ["project_id"],
                },
            },
        },
''',
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_add_task",
                "description": "Add a task to a Project Companion project.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "stage": {"type": "string"},
                        "dependencies": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["project_id", "name", "description", "stage"],
                },
            },
        },
''',
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_update_task_status",
                "description": "Update a Project Companion task status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "task_id": {"type": "string"},
                        "status": {"type": "string"},
                        "result": {"type": "string"},
                        "test_results": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["project_id", "task_id", "status"],
                },
            },
        },
''',
    '''        {
            "type": "function",
            "function": {
                "name": "pc_project_save_checkpoint",
                "description": "Save a Project Companion checkpoint (restoration disabled in GUI).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "label": {"type": "string"},
                    },
                    "required": ["project_id", "label"],
                },
            },
        },
''',
]

# Check if any pc_ declarations exist
if 'pc_project_create' in content:
    print('some pc_ exist')
else:
    # Insert before the closing bracket
    insert_str = ''.join(pc_decls)
    new_content = content[:end] + insert_str + content[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('added')
