import os
import sys
import re
import subprocess


def get_file_add_date(full_path, fmt="%Y.%m.%d"):
    """파일이 최초로 추가(A)된 커밋 날짜를 반환. 수정 커밋은 무시."""
    try:
        result = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--follow', '-1',
             '--format=%ad', f'--date=format:{fmt}', '--', full_path],
            capture_output=True, text=True
        )
        date = result.stdout.strip()
        if date:
            return date
        # untracked 파일(아직 커밋 안 된 신규 파일) 폴백
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ad', f'--date=format:{fmt}', '--', full_path],
            capture_output=True, text=True
        )
        return result.stdout.strip() or "-"
    except Exception:
        return "-"


def get_h1_title(full_path):
    """파일 첫 5줄 내 H1 헤더 텍스트 반환. 없으면 None."""
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        non_empty = [l for l in lines if l.strip()]
        for line in non_empty[:5]:
            if line.startswith("# "):
                return line[2:].strip()
        return None
    except Exception:
        return None


CATEGORY_FOLDERS = ["ai", "algorithm", "db", "devops", "etc", "java", "network", "os", "spring"]


def update_category_readme(base_path, cat_folder):
    """카테고리 폴더의 README.md 목차 테이블을 커밋된 파일 기준으로 갱신."""
    folder_path = os.path.join(base_path, cat_folder)
    readme_path = os.path.join(folder_path, "README.md")

    if not os.path.exists(readme_path):
        print(f"Skip: {cat_folder}/README.md 없음")
        return

    entries = []
    try:
        files = os.listdir(folder_path)
    except Exception:
        return

    for file in sorted(files):
        if not file.endswith(".md") or file.upper() == "README.MD":
            continue
        full_path = os.path.join(folder_path, file)
        if not is_valid_study_note(full_path):
            continue
        date = get_file_add_date(full_path, fmt="%Y-%m-%d")
        if date == "-":
            continue  # 미커밋 파일 제외
        title = get_h1_title(full_path) or file.replace(".md", "")
        entries.append({"date": date, "title": title, "file": file})

    entries.sort(key=lambda x: x["date"])

    table_rows = [
        f"| {i} | {e['title']} | {e['date']} | [바로가기](./{e['file']}) |"
        for i, e in enumerate(entries, 1)
    ]

    new_table = (
        "| 순번 | 제목 | 날짜 | 링크 |\n"
        "| :---: | :--- | :---: | :---: |\n"
        + "\n".join(table_rows)
    )

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- CATEGORY_TABLE_START -->).*?(<!-- CATEGORY_TABLE_END -->)"
    replacement = f"\\1\n{new_table}\n\\2"
    updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"{cat_folder}/README.md updated with {len(entries)} entries.")


def is_valid_study_note(full_path):
    """H1 헤더가 있고 실질적 내용이 5줄 이상인 파일만 유효한 학습 노트로 판단."""
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        non_empty = [l for l in lines if l.strip()]
        has_h1 = any(l.startswith("# ") for l in non_empty[:5])
        return has_h1 and len(non_empty) >= 5
    except Exception:
        return False


def update_readme(member_folder):
    current_dir = os.getcwd()
    base_path = os.path.join(current_dir, member_folder)
    readme_path = os.path.join(base_path, "README.md")

    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} 를 찾을 수 없습니다.")
        return

    EMOJI_MAP = {
        "AI":        "🤖 AI",
        "ALGORITHM": "🔢 Algorithm",
        "CS":        "📖 CS",
        "DB":        "🗄️ DB",
        "DEVOPS":    "♾️ DevOps",
        "ETC":       "📁 Etc",
        "JAVA":      "☕ Java",
        "NETWORK":   "🌐 Network",
        "OS":        "⚙️ OS",
        "SPRING":    "🍃 Spring",
        "INTERVIEW": "🎤 Interview",
        "GENERAL":   "📝 General",
    }

    EXCLUDED_DIRS = {"assets", ".git", "interview"}  # assets: 이미지 전용 폴더, interview: README 노출 제외

    logs = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for file in files:
            if not file.endswith(".md") or file.upper() == "README.MD":
                continue

            full_path = os.path.join(root, file)
            if not is_valid_study_note(full_path):
                print(f"Skip (invalid): {os.path.relpath(full_path, base_path)}")
                continue
            rel_path = os.path.relpath(full_path, base_path)

            # 최상위 서브폴더를 카테고리로 사용
            parts = rel_path.split(os.sep)
            cat_key = parts[0].upper() if len(parts) > 1 else "GENERAL"
            category = EMOJI_MAP.get(cat_key, f"📝 {parts[0].capitalize()}")

            # 파일명 형식: YYMMDD_제목.md 이면 날짜 분리, 아니면 git log 에서 날짜 조회
            stem = file.replace(".md", "")
            date_part = stem.split("_", 1)[0] if "_" in stem else ""
            if re.match(r'^\d{6}$', date_part):
                title_part = stem.split("_", 1)[1]
                date = date_part
                topic = title_part
            else:
                date = get_file_add_date(full_path)
                topic = stem

            logs.append({
                "date":     date,
                "category": category,
                "topic":    topic,
                "path":     rel_path.replace(os.sep, "/"),
            })

    # 최신순 정렬 후 상위 5개만
    logs.sort(key=lambda x: x["date"], reverse=True)
    logs = logs[:5]

    table_rows = [
        f"| {l['date']} | {l['category']} | {l['topic']} | [Go](./{l['path']}) |"
        for l in logs
    ]

    new_table = (
        "| Date | Category | Topic | Link |\n"
        "| :--- | :--- | :--- | :--- |\n"
        + "\n".join(table_rows)
    )

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"(<!-- LOG_TABLE_START -->).*?(<!-- LOG_TABLE_END -->)"
    replacement = f"\\1\n{new_table}\n\\2"
    updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README.md updated with {len(logs)} entries (top 5).")

    for cat in CATEGORY_FOLDERS:
        update_category_readme(base_path, cat)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_readme(sys.argv[1])
    else:
        print("Usage: python update_readme.py <member_folder>")
