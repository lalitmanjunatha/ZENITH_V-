import sys

path = 'zenith_gui.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
old = "from Tools.screen_processor  import _capture_camera, _capture_screen"
new = old + "\n# Project Companion tools \u2014 lazily delegate to agent.py service.\nfrom agent import _pc_project_create, _pc_project_list, _pc_project_state_summary\nfrom agent import _pc_project_add_task, _pc_project_update_task_status\nfrom agent import _pc_project_save_checkpoint"
if 'from agent import _pc_project_create' not in content:
    if old in content:
        content = content.replace(old, new)
        print("imports added")
    else:
        print("import not found")
else:
    print("imports already exist")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
