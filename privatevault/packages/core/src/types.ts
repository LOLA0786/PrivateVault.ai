import { z } from "zod";

export const CostItem = z.object({
  cloud: z.enum(["aws","azure","gcp"]),
  service: z.string(),
  usage_type: z.string().optional().default(""),
  resource_id: z.string().nullable().optional(),
  date: z.coerce.date(),
  cost: z.number()
});
export type CostItem = z.infer<typeof CostItem>;

export const Recommendation = z.object({
  id: z.string(),
  title: z.string(),
  impact_monthly: z.number(),
  effort: z.enum(["low","medium","high"]).default("low"),
  rationale: z.string(),
  actions: z.array(z.string()),
  related: z.array(z.string()).default([]),
  meta: z.record(z.string()).default({})
});
export type Recommendation = z.infer<typeof Recommendation>;
