import { Recommendation, CostItem } from "./types.js";

export function generateRecommendations(items: CostItem[], cloud: "aws"|"azure"|"gcp"): Recommendation[] {
  const svc: Record<string, number> = {};
  let total = 0;
  for (const it of items) {
    svc[it.service] = (svc[it.service] ?? 0) + it.cost;
    total += it.cost;
  }
  total = total || 1;
  const recs: Recommendation[] = [];

  const add = (id: string, title: string, impact: number, rationale: string, actions: string[], effort: "low"|"medium"|"high" = "low") => {
    recs.push({
      id: `${cloud}-${id}`,
      title, impact_monthly: Math.round(impact*100)/100,
      effort, rationale, actions, related: [], meta: { cloud }
    });
  };

  const computePct = Object.entries(svc).filter(([k]) => /(EC2|Compute Engine|Virtual Machines)/.test(k)).reduce((a, [,v]) => a+v, 0) / total;
  if (computePct > 0.30) {
    const savings = computePct * total * 0.12;
    add("rightsizing", "Rightsize Always-On VMs by one tier", savings,
      "Compute >30% of spend; rightsizing typically saves 10–20%.",
      ["Audit CPU/mem <20% for 7d", "Downsize instance family", "Enable autoscaling"]
    );
  }

  const storageSpend = Object.entries(svc).filter(([k]) => /(S3|EBS|Cloud Storage|Blob)/.test(k)).reduce((a, [,v]) => a+v, 0);
  if (storageSpend>0) {
    add("lifecycle", "Enable Lifecycle Policies for cold data", storageSpend*0.12,
      "Tiering/deletion saves 10–20% on object/block storage.",
      ["30d→infrequent; 90d→archive", "Delete expired versions"]
    );
  }

  const egress = Object.entries(svc).filter(([k]) => /(Data Transfer|Egress)/.test(k)).reduce((a, [,v]) => a+v, 0);
  if (egress>0) {
    add("egress", "Reduce cross‑AZ/region egress", egress*0.25,
      "Topology & private links reduce egress by 20–40%.",
      ["Co‑locate resources", "Use CDN", "Consolidate buckets"]
    );
  }

  if (cloud==="aws" && Object.keys(svc).some(k=>/RDS/.test(k))) {
    const rds = Object.entries(svc).filter(([k]) => /RDS/.test(k)).reduce((a, [,v]) => a+v, 0);
    add("rds-ri", "Buy RDS RIs/Savings Plans", rds*0.28,
      "1‑yr RIs/Savings Plans save ~28%.",
      ["Find steady DBs", "Commit 1‑yr no‑upfront"]
    );
  }
  if (cloud==="azure" && Object.keys(svc).some(k=>/(App Service|SQL Database)/.test(k))) {
    add("ahb", "Enable Azure Hybrid Benefit", total*0.05,
      "BYOL reduces compute/SQL cost substantially.",
      ["Validate license", "Toggle AHB where eligible"]
    );
  }
  if (cloud==="gcp" && Object.keys(svc).some(k=>/BigQuery/.test(k))) {
    const bq = Object.entries(svc).filter(([k]) => /BigQuery/.test(k)).reduce((a, [,v]) => a+v, 0);
    add("bq-commit", "Switch BigQuery to flat‑rate commitments", bq*0.30,
      "Committed use discounts lower analytics volatility and cost.",
      ["Estimate slot usage", "Buy flex/monthly commitments"]
    );
  }

  return recs.sort((a,b)=> b.impact_monthly - a.impact_monthly).slice(0,10);
}
