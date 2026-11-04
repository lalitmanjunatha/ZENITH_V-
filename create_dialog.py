path = 'zenith_gui.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'class ProjectCompanionDialog' in content:
    print('exists')
    raise SystemExit

dialog = r'''

class ProjectCompanionDialog:
    """Compact native view for Project Companion."""

    def __init__(self, zenith_live):
        self.zenith_live = zenith_live
        self.zenith_live._pc_dialog = self
        self._current_project_id = None
        self._projects = []
        try:
            self.zenith_live.ui.set_state("LISTENING")
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
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC list error: {err}")
                self._projects = []
                self._show_projects()
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC list exception: {e}")
            self._projects = []
            self._show_projects()

    def _show_projects(self):
        try:
            if not self._projects:
                self.zenith_live.ui.write_log("SYS: PC: No projects found. Create one below.")
                return
            self.zenith_live.ui.write_log(f"SYS: PC: {len(self._projects)} project(s):")
            for p in self._projects:
                pid = p.get("id") or p.get("project_id") or ""
                name = p.get("name") or "Unnamed"
                ptype = p.get("project_type") or p.get("type") or ""
                stage = p.get("stage") or ""
                self.zenith_live.ui.write_log(f"  - {name} [{ptype}] {stage} (id:{pid})")
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
                self.zenith_live.ui.write_log(f"SYS: PC: Created project {name} ({pid})")
                self.refresh_projects()
                return True, pid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC create error: {err}")
                return False, err
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC create exception: {e}")
            return False, str(e)

    def select_project(self, project_id):
        self._current_project_id = project_id
        try:
            svc = get_pc_service()
            res = svc.project_state_summary(project_id)
            if isinstance(res, dict) and res.get("ok"):
                s = res.get("summary") or res
                self.zenith_live.ui.write_log(f"SYS: PC: Selected {project_id}")
                self.zenith_live.ui.write_log(f"  Stage: {s.get('stage')} Tasks:{s.get('tasks_count')} Milestones:{s.get('milestones_count')}")
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC summary error: {err}")
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC select exception: {e}")

    def add_task(self, project_id, name, description, stage, dependencies=None):
        try:
            svc = get_pc_service()
            res = svc.project_add_task(project_id, name, description, stage, dependencies or [])
            if isinstance(res, dict) and res.get("ok"):
                tid = res.get("task_id")
                self.zenith_live.ui.write_log(f"SYS: PC: Added task {name} ({tid})")
                self.refresh_projects()
                return True, tid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC add_task error: {err}")
                return False, err
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC add_task exception: {e}")
            return False, str(e)

    def update_task_status(self, project_id, task_id, status, result="", test_results=None):
        try:
            svc = get_pc_service()
            res = svc.project_update_task_status(project_id, task_id, status, result or "", test_results or [])
            if isinstance(res, dict) and res.get("ok"):
                self.zenith_live.ui.write_log(f"SYS: PC: Task {task_id} -> {status}")
                self.refresh_projects()
                return True
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC update_task error: {err}")
                return False
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC update_task exception: {e}")
            return False

    def save_checkpoint(self, project_id, label):
        try:
            svc = get_pc_service()
            res = svc.project_save_checkpoint(project_id, label)
            if isinstance(res, dict) and res.get("ok"):
                cid = res.get("checkpoint_id")
                self.zenith_live.ui.write_log(f"SYS: PC: Saved checkpoint {label} ({cid})")
                return True, cid
            else:
                err = res.get("error") if isinstance(res, dict) else "unknown"
                self.zenith_live.ui.write_log(f"SYS: PC checkpoint error: {err}")
                return False, err
        except Exception as e:
            self.zenith_live.ui.write_log(f"SYS: PC checkpoint exception: {e}")
            return False, str(e)

    def list_checkpoints(self, project_id):
        try:
            self.zenith_live.ui.write_log("SYS: PC: Checkpoints are stored in project/session data. Use Save Checkpoint to create one.")
            self.zenith_live.ui.write_log("SYS: PC: Checkpoint restoration is DISABLED in this GUI.")
        except Exception:
            pass

'''

# Append to end
content = content.rstrip() + '\n' + dialog
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('added')
