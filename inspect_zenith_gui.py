with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

# Find Project Companion related code
for i in range(len(lines)):
    stripped = lines[i].strip()
    if 'Project Companion' in stripped or 'project_create' in stripped.lower() or 'project_list' in stripped.lower() or 'project_save_checkpoint' in stripped.lower() or 'TOOL_DECLARATIONS' in stripped:
        for j in range(max(0,i-1), min(len(lines), i+2)):
            print(f'{j+1}: {lines[j].rstrip()[:80]}')
        print('---')
PYEOF