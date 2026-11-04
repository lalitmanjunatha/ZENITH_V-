with open('agent.py', 'r', errors='replace') as f:
    lines = f.readlines()

for i in range(len(lines)):
    stripped = lines[i].strip()
    if 'Project Companion' in stripped or 'get_pc_service' in stripped or '_pc_project' in stripped or '_PCService' in stripped:
        for j in range(max(0,i-1), min(len(lines), i+3)):
            print(f'{j+1}: {lines[j].rstrip()[:80]}')
        print('---')