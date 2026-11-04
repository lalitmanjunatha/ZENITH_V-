#!/usr/bin/env python3
"""Add _ReconnectSignal class at the end of zenith_gui.py"""

with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

# _ReconnectSignal class to add at the end
reconnect_signal_class = [
    "\n",
    "class _ReconnectSignal(Exception):",
    '    """Raised inside the session TaskGroup to force a clean, voluntary reconnect',
    '    (e.g. the user picked a new voice — the voice is fixed at connect time, so',
    '    the session must be rebuilt).',
    """    Carries `keep_context`: True for an ordinary rebuild, where the stored resumption handle is replayed and the conversation continues; False when the new session must genuinely start clean (see the voice-change note in _on_voice_change).""",
    "\n",
    "    def __init__(self, keep_context: bool = True):",
    "        super().__init__(),",
    "        self.keep_context = keep_context",
]

# Insert at the end of the file
new_lines = lines + reconnect_signal_class

with open('zenith_gui.py', 'w', errors='replace') as f:
    f.writelines(new_lines)

print(f'_ReconnectSignal class added. New file has {len(new_lines)} lines.')