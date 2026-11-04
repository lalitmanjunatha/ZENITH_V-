path = 'zenith_gui.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

marker = '    def _ui_wake_manual(self)'
if marker in content and 'open_project_companion' not in content:
    idx = content.find(marker)
    line_start = content.rfind('\n', 0, idx) + 1
    method = '''    def open_project_companion(self):
        try:
            if hasattr(self, '_pc_dialog') and self._pc_dialog is not None:
                try:
                    self._pc_dialog.refresh()
                except Exception:
                    pass
                self.ui.write_log("SYS: Project Companion reopened")
                return
        except Exception:
            pass
        try:
            dialog = ProjectCompanionDialog(self)
            self._pc_dialog = dialog
            self.ui.write_log("SYS: Project Companion opened")
        except Exception as e:
            self.ui.write_log(f"SYS: Project Companion error: {e}")

'''
    content = content[:line_start] + method + content[line_start:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('added')
else:
    print('skipped')
