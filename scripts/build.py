import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "lessons"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
SITE_DIR = ROOT / "site"
LESSONS_OUT = SITE_DIR / "lessons"
TOTAL_DAYS = 30

LESSON_META = {
    1: {"minutes": "18 分鐘", "tag": "基礎觀念"},
    2: {"minutes": "16 分鐘", "tag": "開始準備"},
    3: {"minutes": "17 分鐘", "tag": "商品挑選"},
    4: {"minutes": "16 分鐘", "tag": "投入節奏"},
    5: {"minutes": "17 分鐘", "tag": "常見錯誤"},
}

IMAGE_RE = re.compile(r'^!\[(.*?)\]\(([^)\s]+)(?:\s+"([^"]+)")?\)$')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_list = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            close_list()
            continue

        image_match = IMAGE_RE.match(line.strip())
        if image_match:
            close_list()
            alt_text, src, title = image_match.groups()
            figure_parts = ['<figure class="lesson-graphic">']
            desktop_src = None
            caption = title
            if title and title.startswith("desktop:"):
                desktop_src = title.split(":", 1)[1].strip()
                caption = None
            if desktop_src:
                figure_parts.extend([
                    '  <picture>',
                    f'    <source media="(min-width: 981px)" srcset="{html.escape(desktop_src)}">',
                    f'    <img src="{html.escape(src)}" alt="{html.escape(alt_text)}" loading="lazy">',
                    '  </picture>',
                ])
            else:
                figure_parts.append(f'  <img src="{html.escape(src)}" alt="{html.escape(alt_text)}" loading="lazy">')
            if caption:
                figure_parts.append(f'  <figcaption>{html.escape(caption)}</figcaption>')
            figure_parts.append('</figure>')
            out.append("\n".join(figure_parts))
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


def progress_percent(day_num: int) -> str:
    percent = max(0, min(100, (day_num / TOTAL_DAYS) * 100))
    return f"{percent:.1f}"


def lesson_day_label(day_num: int) -> str:
    return f"Day {day_num}"


def lesson_meta(day_num: int) -> dict:
    return LESSON_META.get(day_num, {"minutes": "10 分鐘", "tag": "學習中"})


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
        meta = lesson_meta(day_num)

        prev_link = ""
        next_link = ""

        if idx > 0:
            prev_day_match = re.search(r"day-(\d+)", files[idx - 1].stem)
            prev_day_num = int(prev_day_match.group(1))
            prev_path = files[idx - 1].stem + ".html"
            prev_title = lesson_title_from_markdown(read_text(files[idx - 1]))
            prev_link = (
                f'<a class="lesson-nav-card lesson-nav-card-prev" href="{prev_path}">'
                f'<span class="lesson-nav-label">上一課</span>'
                f'<strong>← {lesson_day_label(prev_day_num)}</strong>'
                f'<span class="lesson-nav-copy">{html.escape(prev_title)}</span>'
                f'</a>'
            )

        if idx < len(files) - 1:
            next_day_match = re.search(r"day-(\d+)", files[idx + 1].stem)
            next_day_num = int(next_day_match.group(1))
            next_path = files[idx + 1].stem + ".html"
            next_title = lesson_title_from_markdown(read_text(files[idx + 1]))
            next_link = (
                f'<a class="lesson-nav-card lesson-nav-card-next" href="{next_path}">'
                f'<span class="lesson-nav-label">下一課</span>'
                f'<strong>{lesson_day_label(next_day_num)} →</strong>'
                f'<span class="lesson-nav-copy">{html.escape(next_title)}</span>'
                f'</a>'
            )

        lesson_inner = (
            lesson_tpl.replace("{{day}}", str(day_num))
            .replace("{{title}}", html.escape(title))
            .replace("{{body}}", body)
            .replace("{{prev_link}}", prev_link)
            .replace("{{next_link}}", next_link)
            .replace("{{progress_percent}}", progress_percent(day_num))
        )

        final = render_base(title, title, lesson_inner, "../")
        out_path = LESSONS_OUT / f"{path.stem}.html"
        write_text(out_path, final)
        lessons.append(
            {
                "day": day_num,
                "title": title,
                "file": out_path.name,
                "minutes": meta["minutes"],
                "tag": meta["tag"],
            }
        )

    return lessons


def build_lesson_rows(lessons: list[dict]) -> str:
    rows = []
    for lesson in lessons:
        rows.append(
            "\n".join(
                [
                    "<tr>",
                    f"  <td data-label=\"天數\">{lesson_day_label(lesson['day'])}</td>",
                    f"  <td data-label=\"主題\">{html.escape(lesson['title'])}</td>",
                    f'  <td data-label="預估時間">{lesson["minutes"]}</td>',
                    f'  <td data-label="重點"><span class="table-tag">{lesson["tag"]}</span></td>',
                    f'  <td data-label="查看內容"><a class="table-link" href="lessons/{lesson["file"]}">開始這一天</a></td>',
                    "</tr>",
                ]
            )
        )
    return "\n".join(rows)


def copy_tree(src_root: Path, dest_root: Path) -> None:
    if not src_root.exists():
        return
    for src in src_root.rglob("*"):
        if src.is_dir():
            continue
        relative = src.relative_to(src_root)
        dest = dest_root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())


def copy_assets() -> None:
    copy_tree(ASSETS_DIR, SITE_DIR / "assets")


def build_index(lessons: list[dict]) -> None:
    content = read_text(TEMPLATES_DIR / "index.html")
    content = content.replace("{{lesson_rows}}", build_lesson_rows(lessons))
    final = render_base(
        "台股新手投資入門",
        "給剛開始接觸台股的人看的投資入門網站",
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
    if SITE_DIR.exists():
        for path in sorted(SITE_DIR.rglob("*"), reverse=True):
            if path.is_file() or path.is_symlink():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    lessons = build_lessons()
    build_index(lessons)
    copy_assets()
    build_static_files()
    print(f"Built site into {SITE_DIR}")


if __name__ == "__main__":
    main()
