# 1. Структура контента и Astro Collections

Для управления проектами и работами необходимо использовать [Astro Content Collections](https://docs.astro.build/en/guides/content-collections/).

## Предлагаемые коллекции

На основе анализа папок в `old/templates/`, мы выделим следующие коллекции:

1. `cartoons` (Мультфильмы)
2. `misc` (Разное)
3. `princess` (Принцесса)
4. `princess_seasons` (Сезоны принцессы)
5. `flat` (Плоская графика)
6. `projects` (Проекты)
7. `comics` (Комиксы)

## Определение схемы (src/content/config.ts)

```typescript
import { defineCollection, z } from 'astro:content';

const baseSchema = z.object({
  hover_text: z.string(),
  url: z.string().optional(), // Пользовательский слаг из старого desc.yaml
  youtube: z.string().optional(),
  width: z.number().optional(),
  height: z.number().optional(),
  pages: z.number().optional(), // Для комиксов
  twitter: z.string().optional(),
  facebook: z.string().optional(),
  the_book: z.string().optional(),
});

export const collections = {
  'cartoons': defineCollection({ type: 'content', schema: baseSchema }),
  'misc': defineCollection({ type: 'content', schema: baseSchema }),
  'princess': defineCollection({ type: 'content', schema: baseSchema }),
  'princess_seasons': defineCollection({ type: 'content', schema: baseSchema }),
  'flat': defineCollection({ type: 'content', schema: baseSchema }),
  'projects': defineCollection({ type: 'content', schema: baseSchema }),
  'comics': defineCollection({ type: 'content', schema: baseSchema }),
};
```

## Формат файлов контента

Каждая запись в коллекции будет представлена файлом `.md` (или `.mdx`).
- **Frontmatter**: Данные из `desc.yaml`.
- **Body**: Содержимое `big_text.html`.

Пример (`src/content/cartoons/1.md`):
```markdown
---
hover_text: "Mosquitoes / Комары"
url: "mosquitoes"
youtube: "http://www.youtube.com/embed/pgC22Su_JOs"
width: 587
height: 439
---
<div>
    <h1>Mosquitoes / Комары</h1>
    ...
</div>
```
