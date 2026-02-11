#!/usr/bin/env python3
import os
import yaml
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'old' / 'templates'
DST_CONTENT = ROOT / 'new' / 'src' / 'content'
DST_ASSETS = ROOT / 'new' / 'src' / 'assets' / 'content'

COLLECTIONS = ['cartoons', 'misc', 'princess', 'princess_seasons', 'flat', 'projects', 'comics']
ASSET_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def ensure_dirs():
    for col in COLLECTIONS:
        (DST_CONTENT / col).mkdir(parents=True, exist_ok=True)


def load_yaml(p: Path):
    if not p.exists():
        return {}
    with p.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def read_html(p: Path):
    if not p.exists():
        return ''
    with p.open('r', encoding='utf-8') as f:
        return f.read()


def copy_media(col: str, item_id: str, item_dir: Path):
    out_dir = DST_ASSETS / col / item_id
    out_dir.mkdir(parents=True, exist_ok=True)
    media = []
    for name in os.listdir(item_dir):
        ext = Path(name).suffix.lower()
        if ext in ASSET_EXT:
            src = item_dir / name
            dst = out_dir / name
            shutil.copy2(src, dst)
            media.append(name)
    return out_dir, media


def guess_images(col: str, item_id: str, media_names):
    # Сопоставление известных имён для frontmatter
    # ВНИМАНИЕ: пути должны быть ОТНОСИТЕЛЬНЫМИ к MD-файлу (`src/content/<col>/<id>.md`),
    # чтобы работал helper image() в Astro. До ассетов путь: ../../assets/content/<col>/<id>/<file>
    base_rel = f"../../assets/content/{col}/{item_id}"
    fm = {}
    for key in ['thumbnail', 'cover', 'full', 'original']:
        for name in media_names:
            if name.lower().startswith(key):
                rel = f"{base_rel}/{name}"
                fm[key if key != 'original' else 'full'] = rel
                break
    # Для комиксов соберём страницы p1.jpg ...
    if col == 'comics':
        pages = []
        for name in sorted(media_names):
            if name.lower().startswith('p') and name.lower().endswith('.jpg'):
                pages.append(f"{base_rel}/{name}")
        if pages:
            fm['pages_images'] = pages
    return fm


def write_md(col: str, item_id: str, yml: dict, html: str, img_fields: dict):
    md_path = DST_CONTENT / col / f"{item_id}.md"
    frontmatter = {**yml}
    # Добавим поля изображений, если обнаружены
    frontmatter.update(img_fields)

    with md_path.open('w', encoding='utf-8') as f:
        f.write('---\n')
        yaml.safe_dump(frontmatter, f, allow_unicode=True, sort_keys=False)
        f.write('---\n\n')
        f.write(html)
    return md_path


def migrate_item(col: str, item_id: str):
    item_dir = SRC / col / item_id
    desc_yaml = item_dir / 'desc.yaml'
    big_html = item_dir / 'big_text.html'

    yml = load_yaml(desc_yaml)
    html = read_html(big_html)
    assets_dir, media = copy_media(col, item_id, item_dir)
    img_fields = guess_images(col, item_id, media)
    write_md(col, item_id, yml, html, img_fields)


def main():
    ensure_dirs()
    for col in COLLECTIONS:
        src_col = SRC / col
        if not src_col.exists():
            continue
        for item_id in os.listdir(src_col):
            if not item_id.isdigit():
                continue
            migrate_item(col, item_id)
    print('Migration finished: content ->', DST_CONTENT)
    print('Migration finished: assets  ->', DST_ASSETS)


if __name__ == '__main__':
    main()
