#!/usr/bin/env python3
with open('zenith_gui.py', 'rb') as f:
    content = f.read()

# Find and fix the corrupted UTF-8 sequence at position 60068
# The corrupted bytes are at position 60068: 0xe2 0x3f 0xb3
# Replace with a simple space or ASCII equivalent

# The corrupted area is around position 60068
# Let's find the exact location and replace
corrupted_pos = 60068

# Replace the 3 corrupted bytes with ASCII 'Co' (for "Coordinate" or similar)
# Actually, let's just replace the whole corrupted sequence with safe ASCII
old_bytes = content[corrupted_pos:corrupted_pos+3]  # 0xe2 0x3f 0xb3
print(f'Corrupted bytes: {old_bytes}')

# Replace with 'Co' (2 ASCII bytes) or a space
# We need to be careful about the replacement length
replacement = b'Co'  # 2 bytes instead of 3 - this will shift everything after it

# Actually, let's replace with a single space and adjust
content = content[:corrupted_pos] + b' ' + content[corrupted_pos+3:]

# Verify the fix
try:
    content.decode('utf-8')
    print('File is now valid UTF-8')
except UnicodeDecodeError as e:
    print(f'Still has error at position {e.start}')

with open('zenith_gui.py', 'wb') as f:
    f.write(content)

print('Fix applied')