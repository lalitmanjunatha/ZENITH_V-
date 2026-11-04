import sys

path = 'zenith_gui.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the dialog class
start = content.find('class ProjectCompanionDialog')
if start == -1:
    print('not found')
    sys.exit(0)

# Find end of class - look for next top-level class
# Scan forward
i = start
n = len(content)
end = n
# Find next \nclass at column 0
# Simple approach: look for \nclass ProjectCompanionDialog is not next, look for \nclass [A-Z]
# But easier: just cut to end of file if it's the last class
# Or look for \nif __name__ or just take reasonable end
# Actually easier to replace from start to a marker
# Look for the last method we added
marker = 'self.zenith_live.ui.write_log("SYS: PC: Checkpoint restoration is DISABLED in this GUI.")'
midx = content.find(marker, start)
if midx != -1:
    # Find end of that line
    nl = content.find('\n', midx)
    if nl != -1:
        end = nl + 1
        # Skip extra blank lines
        while end < n and content[end] in '\n\r':
            end += 1
        # Now replace from start to end
    else:
        end = n
else:
    end = n

new_dialog = '''class ProjectCompanionDialog:
    """Native view for Project Companion (PyQt6-based)."""

    def __init__(self, zenith_live):
        self.zenith_live = zenith_live
        try:
            self.zenith_live._pc_dialog = self
        except Exception:
            pass
        self._current_project_id = None
        self._projects = []
        try:
            self.zenith_live.ui.set_state("LISTENING")
        except Exception:
            pass
        try:
            self.zenith_live.ui.write_log("SYS: Project Companion opened")
        except Exception:
            pass
        self.refresh()

    def refresh(self):
        self.refresh_projects()

    def refresh_projects(self):
        try:
            svc = get_pc_service()
            res = svc.project_list()
            if isinstance(res, dict) and res.get("ok"):
                self._projects = res.get("projects") or []
                self._show_projects()
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Loaded {len(self._projects)} project(s)")
                except Exception:
                    pass
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC list error: {err}")
                except Exception:
                    pass
                self._projects = []
                self._show_projects()
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC list exception: {e}")
            except Exception:
                pass
            self._projects = []
            self._show_projects()

    def _show_projects(self):
        try:
            if not self._projects:
                self.zenith_live.ui.write_log("SYS: PC: No projects found. Use Create Project to start one.")
                return
            self.zenith_live.ui.write_log(f"SYS: PC: {len(self._projects)} project(s):")
            for p in self._projects:
                pid = p.get("id") or p.get("project_id") or ""
                name = p.get("name") or "Unnamed"
                ptype = p.get("project_type") or p.get("type") or ""
                stage = p.get("stage") or ""
                self.zenith_live.ui.write_log(f"  - {name} [{ptype}] [{stage}] id:{pid}")
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC display error: {e}")

    def create_project(self, name, description, project_type, problem_statement="",
                       goals=None, acceptance_criteria=None, constraints=None):
        try:
            svc = get_pc_service()
            res = svc.project_create(name, description, project_type,
                                     problem_statement or "",
                                     goals or [], acceptance_criteria or [], constraints or [])
            if isinstance(res, dict) and res.get("ok"):
                pid = res.get("project_id")
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Created project {name} ({pid})")
                except Exception:
                    pass
                self.refresh_projects()
                return True, pid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC create error: {err}")
                except Exception:
                    pass
                return False, err
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC create exception: {e}")
            except Exception:
                pass
            return False, str(e)

    def select_project(self, project_id):
        self._current_project_id = project_id
        try:
            svc = get_pc_service()
            res = svc.project_state_summary(project_id)
            if isinstance(res, dict) and res.get("ok"):
                s = res.get("summary") or res
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Selected {project_id}")
                    self.zenith_live.ui.write_log(f"  Stage: {s.get('stage')} Tasks:{s.get('tasks_count')} Milestones:{s.get('milestones_count')}")
                    tasks = s.get("tasks") or []
                    if tasks:
                        self.zenith_live.ui.write_log("  Tasks:")
                        for t in tasks:
                            self.zenith_live.ui.write_log(f"    - {t.get('name')} [{t.get('status')}] id:{t.get('id')}")
                    else:
                        self.zenith_live.ui.write_log("  Tasks: (none)")
                except Exception:
                    pass
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC summary error: {err}")
                except Exception:
                    pass
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC select exception: {e}")
            except Exception:
                pass

    def add_task(self, project_id, name, description, stage, dependencies=None):
        try:
            svc = get_pc_service()
            res = svc.project_add_task(project_id, name, description, stage, dependencies or [])
            if isinstance(res, dict) and res.get("ok"):
                tid = res.get("task_id")
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Added task {name} ({tid})")
                except Exception:
                    pass
                self.refresh_projects()
                return True, tid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC add_task error: {err}")
                except Exception:
                    pass
                return False, err
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC add_task exception: {e}")
            except Exception:
                pass
            return False, str(e)

    def update_task_status(self, project_id, task_id, status, result="", test_results=None):
        try:
            svc = get_pc_service()
            res = svc.project_update_task_status(project_id, task_id, status, result or "", test_results or [])
            if isinstance(res, dict) and res.get("ok"):
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Task {task_id} -> {status}")
                except Exception:
                    pass
                try:
                    self.refresh_projects()
                except Exception:
                    pass
                return True
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC update_task error: {err}")
                except Exception:
                    pass
                return False
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC update_task exception: {e}")
            except Exception:
                pass
            return False

    def save_checkpoint(self, project_id, label):
        try:
            svc = get_pc_service()
            res = svc.project_save_checkpoint(project_id, label)
            if isinstance(res, dict) and res.get("ok"):
                cid = res.get("checkpoint_id")
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC: Saved checkpoint {label} ({cid})")
                except Exception:
                    pass
                return True, cid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                try:
                    self.zenith_live.ui.write_log(f"SYS: PC checkpoint error: {err}")
                except Exception:
                    pass
                return False, err
        except Exception as e:
            try:
                self.zenith_live.ui.write_log(f"SYS: PC checkpoint exception: {e}")
            except Exception:
                pass
            return False, str(e)

    def list_checkpoints(self, project_id):
        try:
            self.zenith_live.ui.write_log("SYS: PC: Checkpoints are stored in project/session data.")
            self.zenith_live.ui.write_log("SYS: PC: Checkpoint restoration is DISABLED in this GUI.")
        except Exception:
            pass


'''

new_content = content[:start] + new_dialog + content[end:]
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('done')
