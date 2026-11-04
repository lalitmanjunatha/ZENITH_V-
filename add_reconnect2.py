#!/usr/bin/env python3
with open('zenith_gui.py', 'r', errors='replace') as f:
    lines = f.readlines()

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

with open('zenith_gui.py', 'w', errors='replace') as f:
    f.writelines(lines + reconnect_signal_class)

print(f'_ReconnectSignal class added. New file has {len(lines) + len(reconnect_signal_class)} lines.')