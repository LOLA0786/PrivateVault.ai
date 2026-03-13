import fs from "node:fs";
import { parse } from "csv-parse/sync";
import { CostItem } from "./types.js";

export function loadCsv(path: string, cloud: "aws"|"azure"|"gcp") {
  const raw = fs.readFileSync(path, "utf8");
  const rows = parse(raw, { columns: true, skip_empty_lines: true, trim: true });
  return rows.map((r: any) => CostItem.parse({
    cloud,
    service: r.service,
    usage_type: r.usage_type || "",
    resource_id: r.resource_id || null,
    date: r.date,
    cost: parseFloat(String(r.cost).replace(/\s/g,''))
  }));
}

export function summarizeByService(items: Array<ReturnType<typeof CostItem.parse>>) {
  const agg: Record<string, number> = {};
  for (const it of items) {
    agg[it.service] = (agg[it.service] ?? 0) + it.cost;
  }
  return agg;
}
