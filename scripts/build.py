import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "lessons"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
SITE_DIR = ROOT / "site"
LESSONS_OUT = SITE_DIR / "lessons"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue

        if line.startswith("# "):
            close_list()
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            close_list()
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            close_list()
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_format(line[2:])}</li>")
        elif re.match(r"\d+\. ", line):
            close_list()
            numbered = re.sub(r"^\d+\.\s+", "", line)
            out.append(f"<p>{inline_format(numbered)}</p>")
        else:
            close_list()
            out.append(f"<p>{inline_format(line)}</p>")

    close_list()
    return "\n".join(out)


def inline_format(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_base(title: str, description: str, content: str, base_path: str) -> str:
    tpl = read_text(TEMPLATES_DIR / "base.html")
    return (
        tpl.replace("{{title}}", html.escape(title))
        .replace("{{description}}", html.escape(description))
        .replace("{{content}}", content)
        .replace("{{base_path}}", base_path)
    )


def lesson_title_from_markdown(md: str) -> str:
    first = md.splitlines()[0].strip()
    return first.lstrip("# ").strip()


def build_lessons() -> list[dict]:
    lesson_tpl = read_text(TEMPLATES_DIR / "lesson.html")
    lessons = []
    files = sorted(CONTENT_DIR.glob("day-*.md"))
    for idx, path in enumerate(files):
        md = read_text(path)
        title = lesson_title_from_markdown(md)
        day_match = re.search(r"day-(\d+)", path.stem)
        day_num = int(day_match.group(1)) if day_match else idx + 1
        body = markdown_to_html("\n".join(md.splitlines()[1:]).strip())

        prev_link = ""
        next_link = ""
        if idx > 0:
            prev_path = files[idx - 1].stem + ".html"
            prev_link = f'<a class="btn" href="{prev_path}">← 上一課</a>'
        if idx < len(files) - 1:
            next_path = files[idx + 1].stem + ".html"
            next_link = f'<a class="btn primary" href="{next_path}">下一課 →</a>'

        lesson_inner = (
            lesson_tpl.replace("{{day}}", str(day_num))
            .replace("{{title}}", html.escape(title))
            .replace("{{body}}", body)
            .replace("{{prev_link}}", prev_link)
            .replace("{{next_link}}", next_link)
        )
        final = render_base(title, title, lesson_inner, "../")
        out_path = LESSONS_OUT / f"{path.stem}.html"
        write_text(out_path, final)
        lessons.append({"day": day_num, "title": title, "file": out_path.name})
    return lessons


def copy_assets() -> None:
    for src in ASSETS_DIR.rglob("*"):
        if src.is_dir():
            continue
        relative = src.relative_to(ASSETS_DIR)
        dest = SITE_DIR / "assets" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())


def build_index() -> None:
    content = read_text(TEMPLATES_DIR / "index.html")
    final = render_base(
        "Hermes Stock Learning",
        "台股新手 30 天學習網站",
        content,
        "",
    )
    write_text(SITE_DIR / "index.html", final)


def build_static_files() -> None:
    write_text(SITE_DIR / ".nojekyll", "")
    cname_src = ROOT / "CNAME"
    if cname_src.exists():
        write_text(SITE_DIR / "CNAME", read_text(cname_src))


def main() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    build_lessons()
    build_index()
    copy_assets()
    build_static_files()
    print(f"Built site into {SITE_DIR}")


if __name__ == "__main__":
    main()
