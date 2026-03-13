import Fastify from "fastify";
import cors from "@fastify/cors";
import * as path from "node:path";
import * as fs from "node:fs";
import dotenv from "dotenv";
dotenv.config({ path: path.resolve(process.cwd(), ".env") });

// ---------- Import Core Logic ----------
import { loadCsv } from "@cloudshift/core/src/normalize.js";
import { generateRecommendations } from "@cloudshift/core/src/rules.js";
import { computeLEI } from "@cloudshift/core/src/lei.js";
import { compileActions } from "@cloudshift/core/src/actions-dsl.js";

// ---------- Constants ----------
const PORT = Number(process.env.PORT || 8787);
const DEMO = {
  aws: path.resolve(process.cwd(), "data/sample/aws.csv"),
  azure: path.resolve(process.cwd(), "data/sample/azure.csv"),
  gcp: path.resolve(process.cwd(), "data/sample/gcp.csv"),
};

// ---------- App Setup ----------
const app = Fastify({ logger: true });
await app.register(cors, { origin: true });

function loadItems(provider) {
  const file = DEMO[provider];
  return loadCsv(file, provider);
}

// ---------- API ROUTES ----------
app.get("/health", async () => ({ ok: true, name: "cloudshift-api", version: "0.1.0" }));

// 💰 Razorpay test routes
app.get("/api/check-razorpay", async () => {
  const key = process.env.RAZORPAY_KEY_ID || "not_set";
  return { ok: true, key_id_loaded: !!key, key_id_prefix: key.slice(0, 8) };
});

app.get("/api/payment/order", async () => {
  return { ok: true, orderId: "order_demo_001", amount: 99900 };
});

app.get("/recommendations", async (req) => {
  const p = String((req.query.provider || "aws"));
  const items = loadItems(p);
  const recs = generateRecommendations(items, p);
  const lei = computeLEI(items);
  return { provider: p, lei, recommendations: recs };
});

// ---------- Start ----------
app.listen({ port: PORT, host: "0.0.0.0" }).then(() => {
  console.log(`✅ CloudShift API running on http://localhost:${PORT}`);
});
