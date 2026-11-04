#!/usr/bin/env python3
with open('zenith_gui.py', 'rb') as f:
    content = f.read()

pos = 60048
start = max(0, pos - 20)
end = min(len(content), pos + 20)
chunk = content[start:end]
print('Problem area bytes:', list(chunk[:30]))
try:
    text = chunk.decode('utf-8')
    print('Is valid UTF-8')
except UnicodeDecodeError as e:
    print(f'Decode error at {e.start}')
    print('Repr of first 30 chars:', repr(chunk[:30]))