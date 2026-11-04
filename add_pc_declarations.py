#!/usr/bin/env python3
"""Add Project Companion tool declarations to zenith_gui.py"""

with open('zenith_gui.py', 'r', errors='replace') as f:
    content = f.read()

# 1. Add PC wrapper imports after the screen_processor import
import_section_marker = 'from Tools.screen_processor  import _capture_camera, _capture_screen'
if import_section_marker in content:
    replacements = {
        import_section_marker: import_section_marker + '\n# Project Companion tools — lazily delegate to agent.py service.\nfrom agent import _pc_project_create, _pc_project_list, _pc_project_state_summary\nfrom agent import _pc_project_add_task, _pc_project_update_task_status\nfrom agent import _pc_project_save_checkpoint\n',
    }
    for old, new in replacements.items():
        content = content.replace(old, new, 1)

# 2. Add _pc_tool_declarations inside TOOL_DECLARATIONS
# Find the closing bracket of TOOL_DECLARATIONS and add the PC declarations before it
# Pattern: '    },\n]' followed by blank line and class _ReconnectSignal
pc_declarations_block = '''    # Project Companion tool declarations — lazily delegate to agent.py service.
    **_pc_tool_declarations,
'''

# Find '    },\n]' that closes TOOL_DECLARATIONS and replace with the block plus the closing
# We need to find the specific occurrence - it's after the shutdown_zenith tool
# Let's search for the pattern near the end of TOOL_DECLARATIONS
search_pattern = '        "parameters": {"type": "OBJECT", "properties": {}, "required": []},\\n    },\\n]'
replacement = '''        "parameters": {"type": "OBJECT", "required": []},\\n    },\\n''' + pc_declarations_block + '''    },\\n]'''

# Actually, let's find a simpler way - insert after the last inline tool
# The TOOL_DECLARATIONS list ends with '    },\\n]'
# I'll find it and insert the PC declarations after '    },' but before ']'

# Let me just locate the exact position and insert
import re

# Find TOOL_DECLARATIONS = [
start = content.find('TOOL_DECLARATIONS = [')
if start == -1:
    print('ERROR: Could not find TOOL_DECLARATIONS')
    exit(1)

# Find the closing ] that belongs to TOOL_DECLARATIONS
# It should be followed by a blank line and class _ReconnectSignal
remaining = content[start:]
# Find the closing bracket
close_idx = remaining.find(']')
if close_idx == -1:
    print('ERROR: Could not find closing bracket')
    exit(1)

# The closing ] should be followed by \r\n\r\nclass _ReconnectSignal
after_close = remaining[close_idx:close_idx+30]
print(f'After closing bracket: {after_close}')

# Check if this is the right location
if 'class _ReconnectSignal' in content[start+close_idx:start+close_idx+100]:
    print('Found _ReconnectSignal after TOOL_DECLARATIONS closing bracket')
    
    # Insert the PC declarations before the closing bracket
    # Replace '    },\n]' with the PC block plus '    },\n]'
    old_pattern = '    },\\n]'
    new_pattern = '''    },\n    # Project Companion tool declarations — lazily delegate to agent.py service.\n    **_pc_tool_declarations,\n]'''
    
    # Actually do the replacement
    content = content.replace(old_pattern, new_pattern, 1)
    print('Replaced TOOL_DECLARATIONS closing')
else:
    print('Could not verify _ReconnectSignal location')
    # Just try to find and insert somewhere appropriate
    # Find the last '    },' in the file and add after it
    last_tool = content.rfind('    },')
    if last_tool != -1:
        # Find the next line
        after = content.find('\\n', last_tool)
        if after != -1:
            # Insert after the last tool
            insert_pos = after + 1
            content = content[:insert_pos] + '''    # Project Companion tool declarations — lazily delegate to agent.py service.\n    **_pc_tool_declarations,\n''' + content[insert_pos:]
            print('Inserted PC declarations after last tool')

# Write the modified content
with open('zenith_gui.py', 'w', errors='replace') as f:
    f.write(content)

print('Done!')
"