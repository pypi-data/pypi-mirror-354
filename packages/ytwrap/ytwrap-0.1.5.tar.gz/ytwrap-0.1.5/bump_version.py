import re
import sys

SETUP_PATH = "setup.py"

# バージョン番号を1つ上げる（例: 0.1.0 → 0.1.1）
def bump_version(version: str) -> str:
    parts = version.strip().split(".")
    if not all(p.isdigit() for p in parts):
        raise ValueError("バージョン番号が不正です: " + version)
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)

def main():
    with open(SETUP_PATH, encoding="utf-8") as f:
        setup_code = f.read()

    m = re.search(r'version\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']', setup_code)
    if not m:
        print("setup.py からバージョン番号を検出できませんでした")
        sys.exit(1)
    old_version = m.group(1)
    new_version = bump_version(old_version)

    new_code = re.sub(
        r'(version\s*=\s*["\'])[0-9]+\.[0-9]+\.[0-9]+(["\'])',
        r'\g<1>' + new_version + r'\2',
        setup_code
    )

    with open(SETUP_PATH, "w", encoding="utf-8") as f:
        f.write(new_code)

    print(f"バージョンを {old_version} → {new_version} に更新しました")

if __name__ == "__main__":
    main()
