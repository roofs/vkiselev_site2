# 4. Фронтенд, лейауты и стили

## Лейауты (`src/layouts/`)
Создать основной лейаут `Layout.astro`, который будет содержать общую структуру HTML, мета-теги для SEO (OpenGraph из старого кода) и навигацию.

Пример структуры `src/layouts/Layout.astro`:
```astro
---
interface Props {
  title: string;
  description?: string;
  image?: string;
}
const { title, description, image } = Astro.props;
---
<html>
  <head>
    <title>{title}</title>
    <!-- Мета-теги для Facebook/Twitter, как в старом cartoon.html -->
    <meta property="og:title" content={title} />
    {description && <meta property="og:description" content={description} />}
    {image && <meta property="og:image" content={image} />}
  </head>
  <body>
    <header>...</header>
    <slot />
    <footer>...</footer>
  </body>
</html>
```

## Компоненты (`src/components/`)
- `ProjectCard.astro` — для отображения плитки проекта (использует `thumbnail.jpg` и `hover_text`).
- `VideoEmbed.astro` — для вставки YouTube видео (на основе логики `process_video_url`).
- `Navigation.astro` — главное меню.

## Стили
В старом проекте использовался Bootstrap (`col-md-3`, `col-sm-4`). 
- **Рекомендация**: Установить Tailwind CSS в Astro (`npx astro add tailwind`). Это позволит быстро воссоздать сетку.
- Если нужно сохранить старый CSS, его можно положить в `src/styles/global.css` и импортировать в лейаут.

## Специфические страницы
- **Комиксы**: На странице комикса нужно реализовать цикл по страницам (поле `pages` из метаданных), формируя пути к изображениям `/comics/<id>/p<index>.jpg`.
- **Принцесса**: Обратить внимание на сортировку (в некоторых разделах используется `reverse=False`).
