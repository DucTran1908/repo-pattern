"""PreToolUse guard for shell tools (Bash, PowerShell).

Heuristic companion to guard_local.py: catches the common ways a shell command
writes into the protected local workspace folders, leaks local paths into
commit messages, or force-adds the ignored workspace to git. It cannot catch
everything; CLAUDE.md remains the primary rule.
"""
import re

from _common import INDEX_FILE, run_pre_tool, worst

PROTECTED = {"design_system": "deny", "test": "ask", "plan": "ask"}

SEGMENT_SPLIT = re.compile(r"&&|\|\||[;\n|]")
PROTECTED_REF = re.compile(r"(?<![\w.-])\.local[/\\](design_system|test|plan)((?:[/\\][^\s\"'|;&<>]*)?)")
WHOLE_LOCAL = re.compile(r"(?<![\w.-])\.local[/\\]?(?=[\s\"']|$)")
REDIRECT_TARGET = re.compile(r">{1,2}\s*[\"']?([^\s\"']+)")
MUTATING_VERB = re.compile(
    r"(?:^|[\s(&])(rm|rmdir|mv|tee|touch|truncate|dd|del|erase|Set-Content|Add-Content|Out-File|"
    r"Remove-Item|Move-Item|Rename-Item|New-Item|Clear-Content|ri|rni)(?=\s|$)",
    re.IGNORECASE,
)
SED_INPLACE = re.compile(r"(?:^|\s)sed\b.*\s(?:-i|--in-place)", re.IGNORECASE)
COPY_VERB = re.compile(r"(?:^|[\s(&])(cp|copy|Copy-Item|cpi|rsync)(?=\s)", re.IGNORECASE)
GIT_COMMIT = re.compile(r"\bgit\s+commit\b")
GIT_FORCE_ADD = re.compile(r"\bgit\s+add\b.*\s(?:-f|--force)\b")
LOCAL_ANY = re.compile(r"(?<![\w.-])\.local(?:[/\\]|\b)")

REASONS = {
    "deny": ("design_system holds the user's exact requirements and is read-only for agents. "
             "Report the blocker and propose a change instead."),
    "ask": "This command modifies protected local workspace data (test data or a plan); user approval required.",
}


def _is_index(rest):
    return rest.strip("/\\") == INDEX_FILE


def _refs(text):
    return [(m.group(1), m.group(2)) for m in PROTECTED_REF.finditer(text)]


def _decision_for(refs):
    return worst(*[PROTECTED[sub] for sub, rest in refs if not _is_index(rest)])


def _segment_decision(seg):
    decisions = []

    if GIT_COMMIT.search(seg) and LOCAL_ANY.search(seg):
        decisions.append(("ask", "Commit messages must not reference local workspace content."))
    if GIT_FORCE_ADD.search(seg) and LOCAL_ANY.search(seg):
        decisions.append(("deny", "The local workspace is never tracked by git."))

    for target in REDIRECT_TARGET.findall(seg):
        d = _decision_for(_refs(target))
        if d:
            decisions.append((d, REASONS[d]))

    if MUTATING_VERB.search(seg) or SED_INPLACE.search(seg):
        d = _decision_for(_refs(seg))
        if d:
            decisions.append((d, REASONS[d]))
        if MUTATING_VERB.search(seg) and WHOLE_LOCAL.search(seg):
            decisions.append(("deny", "Removing or moving the whole local workspace is not allowed."))

    if COPY_VERB.search(seg):
        args = [t.strip("\"'") for t in seg.split() if not t.startswith("-")]
        if args:
            d = _decision_for(_refs(args[-1]))
            if d:
                decisions.append((d, REASONS[d]))

    if not decisions:
        return None, ""
    top = worst(*[d for d, _ in decisions])
    return top, next(r for d, r in decisions if d == top)


def decide(payload, root):
    command = (payload.get("tool_input") or {}).get("command", "")
    if not command:
        return None, ""
    results = [_segment_decision(seg) for seg in SEGMENT_SPLIT.split(command)]
    top = worst(*[d for d, _ in results])
    if top is None:
        return None, ""
    return top, next(r for d, r in results if d == top)


if __name__ == "__main__":
    run_pre_tool(decide)
