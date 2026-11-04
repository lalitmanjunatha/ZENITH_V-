#!/usr/bin/env python3
with open('zenith_gui.py', 'rb') as f:
    content = f.read()

# Search for the corrupted UTF-8 sequence 0xe2 0x3f 0xb3
pattern = b'\xe2\x3f\xb3'
pos = content.find(pattern)
print(f'Pattern found at position: {pos}')

if pos >= 0:
    # Replace with ASCII 'Co' (or just a space)
    # Let's replace with a single space character
    replacement = b' '
    content = content[:pos] + replacement + content[pos+3:]
    
    # Verify
    try:
        content.decode('utf-8')
        print('File is now valid UTF-8')
    except UnicodeDecodeError as e:
        print(f'Still has error at position {e.start}')
    
    with open('zenith_gui.py', 'wb') as f:
        f.write(content)
    print('Fix applied')
else:
    print('Pattern not found')