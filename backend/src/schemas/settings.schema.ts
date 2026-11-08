import { z } from 'zod';

export const settingsSchema = z.object({
    minMoistureThreshold: z.number().min(10).max(50)
});