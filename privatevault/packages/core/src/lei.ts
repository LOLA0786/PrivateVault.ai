// Lock‑in Escape Index (LEI) — heuristic score 0..100 (higher = easier to escape)
import { CostItem } from "./types.js";

export function computeLEI(items: CostItem[]): number {
  // Simple heuristic: more spend on standard services => easier to escape
  let score = 50;
  const addIf = (regex: RegExp, points: number) => {
    if (items.some(i => regex.test(i.service))) score += points;
  };
  addIf(/(EC2|Compute Engine|Virtual Machines)/, 10);  // generic compute
  addIf(/(S3|Cloud Storage|Blob)/, 10);                 // generic object storage
  addIf(/(PostgreSQL|RDS|SQL Database|Cloud SQL)/, 10);// SQL dbs
  addIf(/(Lambda|Functions|App Service)/, -10);        // proprietary PaaS reduce LEI
  addIf(/(BigQuery|CosmosDB|DynamoDB)/, -15);
  return Math.max(0, Math.min(100, score));
}
