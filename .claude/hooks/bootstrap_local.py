"""SessionStart hook: ensures the local workspace layout exists and reports open plans."""
import json
import os
import re

from _common import INDEX_FILE, LOCAL_DIR, SUBFOLDERS, git, project_root, read_payload

INDEX_TEMPLATE = "# {name}\n\n| Path | Description |\n|---|---|\n"
CHECKBOX = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\[( |x|X|~)\]", re.MULTILINE)


def ensure_local(root):
    """Creates missing subfolders and index files; returns the index files created."""
    created = []
    for sub in SUBFOLDERS:
        folder = os.path.join(root, LOCAL_DIR, sub)
        os.makedirs(folder, exist_ok=True)
        index = os.path.join(folder, INDEX_FILE)
        if not os.path.exists(index):
            with open(index, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(INDEX_TEMPLATE.format(name=sub))
            created.append(index)
    return created


def plan_progress(root):
    """Returns [(file name, done, total)] for plans that still have open items."""
    folder = os.path.join(root, LOCAL_DIR, "plan")
    result = []
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if name == INDEX_FILE or not name.endswith(".md"):
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as fh:
            states = CHECKBOX.findall(fh.read())
        done = sum(1 for s in states if s != " ")
        if states and done < len(states):
            result.append((name, done, len(states)))
    return result


def build_context(root, created):
    branch = git(root, "branch", "--show-current").strip() or "(detached or no git)"
    lines = ["Local workspace ready. Current git branch: {}.".format(branch)]
    if created:
        lines.append("Created missing index files: {}.".format(
            ", ".join(os.path.relpath(p, root).replace("\\", "/") for p in created)))
    progress = plan_progress(root)
    if progress:
        lines.append("Plans with open checklist items:")
        lines += ["- {}: {}/{} done".format(n, d, t) for n, d, t in progress]
    return "\n".join(lines)


def main():
    try:
        payload = read_payload()
        root = project_root(payload)
        created = ensure_local(root)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": build_context(root, created),
            }
        }))
    except Exception:
        return


if __name__ == "__main__":
    main()
