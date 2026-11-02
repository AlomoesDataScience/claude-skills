"""Stand-in: the guard moved to the generic game-ui skill (gameui.py at the project root's
.claude/skills/game-ui/scripts). `python3 -I dom6ui.py ...` and `import dom6ui` still work."""
import os
import runpy
import sys

def _skill_scripts(name):
    """scripts/ of a skill in this or any parent folder's .claude/skills (generic skills sit at the root)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        p = os.path.join(d, ".claude", "skills", name, "scripts")
        if os.path.isdir(p) or os.path.dirname(d) == d:
            return p
        d = os.path.dirname(d)

_G = _skill_scripts("game-ui")
os.environ.setdefault("UI_DEFAULT_WMCLASS", "dom6_amd64")   # game-ui has no default window; Dominions' tools mean Dominions
sys.path.insert(0, _G)
if __name__ == "__main__":
    sys.argv[0] = os.path.join(_G, "gameui.py")
    runpy.run_path(sys.argv[0], run_name="__main__")
else:
    import gameui
    sys.modules[__name__] = gameui
