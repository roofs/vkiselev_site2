# Общий план миграции с Python (Google App Engine) на Astro

Этот документ описывает общую стратегию переноса сайта vkiselev.com на фреймворк Astro.

## Цели миграции
- Сохранение структуры ссылок (SEO-friendly).
- Использование современных инструментов разработки (Astro, TypeScript, Tailwind).
- Перенос контента в Astro Collections для удобного управления.
- Статическая генерация для высокой производительности.

## Этапы миграции
1. [01-content-structure.md](./01-content-structure.md) — Описание структуры контента и коллекций.
2. [02-data-migration.md](./02-data-migration.md) — Скрипт и процесс переноса данных и медиа-файлов.
3. [03-routing-and-pages.md](./03-routing-and-pages.md) — Настройка роутинга и создание страниц.
4. [04-frontend-and-layouts.md](./04-frontend-and-layouts.md) — Перенос дизайна и стилей.

## Текущее состояние
- Исходники старого сайта: `/old`
- Начальный проект Astro: `/new`
