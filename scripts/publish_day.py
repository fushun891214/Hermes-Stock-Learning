#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "lessons"
SSH_KEY = Path("/opt/data/.ssh/hermes_stock_learning_ed25519")


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True, env=env)


def lesson_path(day_arg: str) -> Path:
    digits = re.sub(r"\D", "", day_arg)
    if not digits:
        raise SystemExit(f"無法解析 day: {day_arg}")
    day_num = int(digits)
    return CONTENT_DIR / f"day-{day_num:02d}.md"


def commit_message(day_num: int) -> str:
    return f"Update Day {day_num} lesson"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build, commit, and push a day lesson update.")
    parser.add_argument("day", help="Day number, e.g. 1 or day-01")
    parser.add_argument("--message", help="Custom commit message")
    args = parser.parse_args()

    path = lesson_path(args.day)
    day_num = int(re.sub(r"\D", "", args.day))
    if not path.exists():
        raise SystemExit(f"找不到課程檔案：{path}")

    run([sys.executable, "scripts/build.py"])
    run(["git", "add", "-A"])

    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        print("沒有變更可提交。")
        return 0

    message = args.message or commit_message(day_num)
    run(["git", "commit", "-m", message])

    env = os.environ.copy()
    if SSH_KEY.exists():
        env["GIT_SSH_COMMAND"] = f"ssh -i {SSH_KEY} -o IdentitiesOnly=yes"
    run(["git", "push", "origin", "main"], env=env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
