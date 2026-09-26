"""PreToolUse guard for file-editing tools (Edit, Write, MultiEdit, NotebookEdit).

Rules for the local workspace:
  design_system/  user's raw requirements   -> deny (report blockers instead)
  test/           user's test data          -> ask
  plan/           approved plans            -> new file ok; overwrite/other edits ask;
                                               in-order `[ ]` -> `[x]` ticks pass through
  README.md in any subfolder is the index and may always be updated.

Tracked source files must not reference local workspace content; only the
framework files listed in FRAMEWORK_FILES may describe its conventions.
"""
import os
import re

from _common import INDEX_FILE, local_location, rel_to_root, run_pre_tool

FRAMEWORK_FILES = ("CLAUDE.md", "README.md", ".gitignore", "docs/workflow.md")
FRAMEWORK_PREFIXES = (".claude/",)

LOCAL_REF = re.compile(r"(?<![\w.-])\.local[/\\]")
CHECKBOX = re.compile(r"^(\s*(?:[-*+]|\d+\.)\s+)\[( |x|X|~)\](.*)$")
DONE = ("x", "X", "~")


def _target_path(tool_input):
    return tool_input.get("file_path") or tool_input.get("notebook_path") or ""


def _new_text(tool_name, tool_input):
    if tool_name == "Write":
        return tool_input.get("content", "")
    if tool_name == "Edit":
        return tool_input.get("new_string", "")
    if tool_name == "MultiEdit":
        return "\n".join(e.get("new_string", "") for e in tool_input.get("edits", []))
    if tool_name == "NotebookEdit":
        return tool_input.get("new_source", "")
    return ""


def _apply_edits(content, edits):
    for edit in edits:
        old, new = edit.get("old_string", ""), edit.get("new_string", "")
        if not old or old not in content:
            return None
        content = content.replace(old, new) if edit.get("replace_all") else content.replace(old, new, 1)
    return content


def _ticks_only(old, new):
    """Returns indexes of newly ticked lines if the change is only `[ ]` -> `[x]`, else None."""
    old_lines, new_lines = old.splitlines(), new.splitlines()
    if len(old_lines) != len(new_lines):
        return None
    ticked = []
    for i, (a, b) in enumerate(zip(old_lines, new_lines)):
        if a == b:
            continue
        ma, mb = CHECKBOX.match(a), CHECKBOX.match(b)
        if not (ma and mb and ma.group(2) == " " and mb.group(2) in ("x", "X")):
            return None
        if (ma.group(1), ma.group(3)) != (mb.group(1), mb.group(3)):
            return None
        ticked.append(i)
    return ticked or None


def _ticks_in_order(lines, ticked):
    """Every checkbox above a ticked one, within the same heading section, must be done."""
    for idx in ticked:
        for j in range(idx - 1, -1, -1):
            line = lines[j]
            if line.lstrip().startswith("#"):
                break
            m = CHECKBOX.match(line)
            if m and m.group(2) not in DONE:
                return False
    return True


def _decide_plan(tool_name, tool_input, full_path):
    exists = os.path.isfile(full_path)
    if tool_name == "Write":
        if not exists:
            return None, ""
        return "ask", "Overwriting an existing plan requires user approval."
    if not exists:
        return "ask", "Plan file does not exist; plan edits require user approval."
    if tool_name == "Edit":
        edits = [tool_input]
    elif tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
    else:
        return "ask", "Plan edits require user approval."
    with open(full_path, encoding="utf-8") as fh:
        current = fh.read()
    updated = _apply_edits(current, edits)
    if updated is None:
        return None, ""  # the edit itself will fail; nothing to guard
    ticked = _ticks_only(current, updated)
    if ticked is None:
        return "ask", ("Only ticking checklist items ([ ] -> [x]) is allowed without approval. "
                       "Skipping items ([~]) or changing plan content requires user approval.")
    if not _ticks_in_order(updated.splitlines(), ticked):
        return "ask", ("Checklist items must be ticked in order; an earlier item is still open. "
                       "Skipping ahead requires user approval.")
    return None, ""


def _is_framework_file(rel):
    return rel in FRAMEWORK_FILES or rel.startswith(FRAMEWORK_PREFIXES)


def decide(payload, root):
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    path = _target_path(tool_input)
    if not path:
        return None, ""

    loc = local_location(path, root)
    if loc is not None:
        sub, rest = loc
        if rest == INDEX_FILE:
            return None, ""
        if sub == "design_system":
            return "deny", ("design_system holds the user's exact requirements and is read-only for agents. "
                            "Report the blocker to the user and propose a change instead.")
        if sub == "test":
            return "ask", "test holds user-provided test data; edit only when the user explicitly asked."
        if sub == "plan":
            return _decide_plan(tool_name, tool_input, os.path.join(root, path))
        return None, ""

    rel = rel_to_root(path, root)
    if rel is None or _is_framework_file(rel):
        return None, ""
    if LOCAL_REF.search(_new_text(tool_name, tool_input)):
        return "ask", ("Tracked source must not reference local workspace content (.local/...). "
                       "Remove the reference or confirm it is intended.")
    return None, ""


if __name__ == "__main__":
    run_pre_tool(decide)
