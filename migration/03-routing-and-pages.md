# 3. Настройка роутинга и создание страниц

Для сохранения структуры ссылок необходимо настроить динамические роуты в Astro.

## Главная страница (`src/pages/index.astro`)
Должна отображать случайные или выбранные работы из разных коллекций, как это реализовано в `old/main.py` в функции `hello()`.

## Основные разделы
- `/animated` -> `src/pages/animated.astro` (собирает данные из `cartoons`, `misc`, `princess`, `princess_seasons`)
- `/still` -> `src/pages/still.astro` (собирает данные из `flat`, `projects`, `comics`)
- `/memories` -> `src/pages/memories.astro`
- `/vasili` -> `src/pages/vasili.astro`

## Динамические страницы айтемов
Для каждого раздела создаем динамический роут. Например, для мультфильмов:
`src/pages/cartoons/[...slug].astro`

### Логика получения слага для сохранения ссылок:
В старом приложении путь формировался как `/<collection>/<url_from_yaml>` или `/<collection>/<id>`.

```astro
---
// src/pages/cartoons/[...slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const entries = await getCollection('cartoons');
  return entries.map(entry => ({
    params: { 
      // Если в frontmatter есть url, используем его, иначе ID папки
      slug: entry.data.url || entry.id 
    },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
---
<Layout title={entry.data.hover_text}>
  <Content />
</Layout>
```

Аналогично создаются файлы для других коллекций:
- `src/pages/misc/[...slug].astro`
- `src/pages/princess/[...slug].astro`
- `src/pages/princess_seasons/[...slug].astro`
- `src/pages/flat/[...slug].astro`
- `src/pages/projects/[...slug].astro`
- `src/pages/comics/[...slug].astro`

## Пагинация и навигация (Next/Prev)
Функция `get_next_prev` из старого `main.py` должна быть реализована в Astro при генерации путей `getStaticPaths` или с помощью логики обхода коллекции, чтобы на странице работы были ссылки на "предыдущую" и "следующую" работы в рамках той же коллекции.
