import { defineCollection, z } from 'astro:content';

const baseSchema = ({ image }: { image: any }) => z.object({
  hover_text: z.union([z.string(), z.number()]).nullable().optional(),
  url: z.string().nullable().optional(),
  youtube: z.string().nullable().optional(),
  width: z.number().nullable().optional(),
  height: z.number().nullable().optional(),
  pages: z.number().nullable().optional(),
  twitter: z.string().nullable().optional(),
  facebook: z.string().nullable().optional(),
  the_book: z.string().nullable().optional(),
  thumbnail: image().optional(),
  cover: image().optional(),
  full: image().optional(),
  pages_images: z.array(image()).optional(),
});

export const collections = {
  cartoons: defineCollection({ type: 'content', schema: baseSchema }),
  misc: defineCollection({ type: 'content', schema: baseSchema }),
  princess: defineCollection({ type: 'content', schema: baseSchema }),
  princess_seasons: defineCollection({ type: 'content', schema: baseSchema }),
  flat: defineCollection({ type: 'content', schema: baseSchema }),
  projects: defineCollection({ type: 'content', schema: baseSchema }),
  comics: defineCollection({ type: 'content', schema: baseSchema }),
};
