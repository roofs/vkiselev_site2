# 2. Перенос данных и медиа-файлов

Для автоматизации процесса рекомендуется использовать Python-скрипт, который пройдет по всем папкам в `old/templates/` и создаст соответствующие файлы в `new/src/content/`.

## Шаги миграции контента

1. **Конвертация YAML/HTML в MD**:
   - Читаем `desc.yaml` для получения метаданных.
   - Читаем `big_text.html` для получения тела контента.
   - Создаем `.md` файл в `new/src/content/<collection>/<id>.md`.
   - Если в `desc.yaml` есть поле `url`, оно будет использоваться как слаг (slug) для страницы.

2. **Перенос изображений**:
   - Изображения из папок `old/templates/<collection>/<id>/` (например, `thumbnail.jpg`, `full.jpg`, `cover.jpg`, `p1.jpg`...) нужно перенести.
   - **Вариант А (Простой)**: Перенести в `new/public/<collection>/<id>/`. Тогда ссылки в коде будут `/cartoons/1/thumbnail.jpg`.
   - **Вариант Б (Astro-way)**: Перенести в `new/src/assets/content/<collection>/<id>/` для оптимизации изображений средствами Astro.

## Скрипт миграции (набросок на Python)

```python
import os
import yaml
import shutil

src_root = 'old/templates'
dst_root = 'new/src/content'
media_root = 'new/public'

collections = ['cartoons', 'misc', 'princess', 'princess_seasons', 'flat', 'projects', 'comics']

for col in collections:
    col_path = os.path.join(src_root, col)
    if not os.path.exists(col_path): continue
    
    os.makedirs(os.path.join(dst_root, col), exist_ok=True)
    
    for item_id in os.listdir(col_path):
        if not item_id.isdigit(): continue
        
        item_path = os.path.join(col_path, item_id)
        desc_file = os.path.join(item_path, 'desc.yaml')
        text_file = os.path.join(item_path, 'big_text.html')
        
        if os.path.exists(desc_file):
            with open(desc_file, 'r') as f:
                data = yaml.safe_load(f)
            
            with open(text_file, 'r') as f:
                content = f.read()
            
            # Создаем MD файл
            md_path = os.path.join(dst_root, col, f"{item_id}.md")
            with open(md_path, 'w') as f:
                f.write("---\n")
                yaml.dump(data, f, allow_unicode=True)
                f.write("---\n\n")
                f.write(content)
                
            # Копируем картинки в public
            dst_media_path = os.path.join(media_root, col, item_id)
            os.makedirs(dst_media_path, exist_ok=True)
            for img in os.listdir(item_path):
                if img.endswith(('.jpg', '.png', '.gif')):
                    shutil.copy2(os.path.join(item_path, img), os.path.join(dst_media_path, img))
```

## Статические файлы из `old/static`
Файлы из `old/static` (CSS, JS, иконки) следует перенести в `new/public/` или интегрировать в соответствующие компоненты Astro.
