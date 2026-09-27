"""Shared helpers for the project's Claude Code hooks (stdlib only, Python 3.8+)."""
import json
import os
import subprocess
import sys

LOCAL_DIR = ".local"
SUBFOLDERS = ("plan", "project-requirements", "report", "reference", "test", "temp", "session_log")
INDEX_FILE = "README.md"

_SEVERITY = {None: 0, "ask": 1, "deny": 2}


def read_payload():
    """Reads the hook payload from stdin; returns {} when it is not a JSON object."""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def project_root(payload):
    return os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()


def rel_to_root(path, root):
    """Returns `path` relative to `root` with forward slashes, or None when outside it."""
    if not path:
        return None
    full = os.path.abspath(os.path.join(root, path))
    try:
        rel = os.path.relpath(full, os.path.abspath(root))
    except ValueError:  # different drive on Windows
        return None
    rel = rel.replace("\\", "/")
    if rel == ".." or rel.startswith("../"):
        return None
    return rel


def local_location(path, root):
    """Maps a path to (subfolder, rest) when it lives in the local workspace, else None."""
    rel = rel_to_root(path, root)
    if rel is None:
        return None
    parts = rel.split("/")
    if parts[0] != LOCAL_DIR:
        return None
    sub = parts[1] if len(parts) > 1 else ""
    rest = "/".join(parts[2:])
    return sub, rest


def worst(*decisions):
    """Picks the most restrictive decision (deny > ask > None)."""
    return max(decisions, key=lambda d: _SEVERITY[d]) if decisions else None


def emit_pre_tool(decision, reason):
    if decision is None:
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))


def git(root, *args):
    """Runs git and returns stdout, or '' on any failure."""
    try:
        proc = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8", timeout=10
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout if proc.returncode == 0 else ""


def run_pre_tool(decide):
    """Standard PreToolUse entry point: fail open on unexpected errors."""
    try:
        payload = read_payload()
        if not payload:
            return
        decision, reason = decide(payload, project_root(payload))
        emit_pre_tool(decision, reason)
    except Exception:  # never break the session because of a hook bug
        return
