import { defineCollection, z } from 'astro:content';

const baseSchema = ({ image }: { image: any }) => z.object({
  hover_text: z.string(),
  url: z.string().optional(),
  youtube: z.string().optional(),
  width: z.number().optional(),
  height: z.number().optional(),
  pages: z.number().optional(),
  twitter: z.string().optional(),
  facebook: z.string().optional(),
  the_book: z.string().optional(),
  thumbnail: image().optional(),
  cover: image().optional(),
  full: image().optional(),
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
