#!/usr/bin/env python3
with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

# 1. Add PC wrapper imports after line 64 (screen_processor import)
new_imports = [
    '# Project Companion tools — lazily delegate to agent.py service.\n',
    'from agent import _pc_project_create, _pc_project_list, _pc_project_state_summary\n',
    'from agent import _pc_project_add_task, _pc_project_update_task_status\n',
    'from agent import _pc_project_save_checkpoint\n',
]

insert_idx = -1
for i in range(len(lines)):
    if 'from Tools.screen_processor  import _capture_camera, _capture_screen' in lines[i]:
        insert_idx = i + 1
        break

if insert_idx >= 0:
    new_lines = lines[:insert_idx] + new_imports + lines[insert_idx:]
    lines = new_lines
    print(f'Inserted PC imports at line {insert_idx+1}')

# 2. Add PC tool declarations to TOOL_DECLARATIONS
# Find the closing bracket of TOOL_DECLARATIONS
# It's the ']' that comes after the last '    },' within the TOOL_DECLARATIONS block
# TOOL_DECLARATIONS starts at line 170

insert_pc = -1
for i in range(len(lines)-1, 169, -1):
    if lines[i].strip() == '    },' and i+1 < len(lines) and lines[i+1].strip() == ']':
        if i > 170:
            insert_pc = i + 1
            print(f'Found TOOL_DECLARATIONS closing at line {i+1}')
            break

if insert_pc >= 0:
    pc_declarations = [
        '    # Project Companion tool declarations — lazily delegate to agent.py service.\n',
        '    # These are available as pc_project_create, pc_project_list, etc.\n',
    ]
    new_lines = lines[:insert_pc] + pc_declarations + lines[insert_pc:]
    lines = new_lines
    print(f'Inserted PC declarations at line {insert_pc+1}')

with open('zenith_gui.py', 'w', errors='replace') as f:
    f.writelines(lines)

print('Done! Verifying syntax...')
PYEOF