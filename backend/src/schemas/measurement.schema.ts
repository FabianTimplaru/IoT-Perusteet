import { z } from 'zod';

export const measurementSchema = z.object({
    moisture: z.number().min(0).max(100),
    airHumidity: z.number().min(0).max(100),
    temperature: z.number().min(0).max(50),
    rawAdc: z.number().int().min(0).max(4095)
});