"""Stop hook: asks the agent to update the session log after changing tracked files.

Blocks (once) when a changed file in the working tree is newer than the newest
session log. `stop_hook_active` prevents loops.
"""
import glob
import json
import os

from _common import INDEX_FILE, LOCAL_DIR, git, project_root, read_payload


def changed_files_from_git(root):
    out = git(root, "status", "--porcelain", "--untracked-files=all")
    files = []
    for line in out.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.append(path.strip('"'))
    return files


def newest_log_mtime(root):
    logs = [p for p in glob.glob(os.path.join(root, LOCAL_DIR, "session_log", "*.md"))
            if os.path.basename(p) != INDEX_FILE]
    return max((os.path.getmtime(p) for p in logs), default=0.0)


def decide(payload, root, changed_files=None):
    if payload.get("stop_hook_active"):
        return None
    if changed_files is None:
        changed_files = changed_files_from_git(root)
    mtimes = [os.path.getmtime(os.path.join(root, f)) for f in changed_files
              if os.path.isfile(os.path.join(root, f))]
    if not mtimes or max(mtimes) <= newest_log_mtime(root):
        return None
    return {
        "decision": "block",
        "reason": ("Files changed since the last session log entry. Update the session log in "
                   ".local/session_log/ (use the session-log skill) with the decisions and changes "
                   "made, then finish. If nothing worth logging happened, say so briefly and stop."),
    }


def main():
    try:
        payload = read_payload()
        result = decide(payload, project_root(payload))
        if result:
            print(json.dumps(result))
    except Exception:
        return


if __name__ == "__main__":
    main()
