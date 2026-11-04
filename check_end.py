with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

# Find the line with 'if __name__ == "__main__"'
last_idx = -1
for i in range(len(lines)):
    if 'if __name__' in lines[i]:
        last_idx = i

# Show the end of file
print(f'Last __main__ at line {last_idx+1}')
print(f'Line {last_idx+1}: {lines[last_idx].rstrip()[:80]}')
if last_idx + 1 < len(lines):
    print(f'Line {last_idx+2}: {lines[last_idx+1].rstrip()[:80]}')