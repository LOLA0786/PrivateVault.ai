#!/bin/bash
set -e
REPO=~/PrivateVault.ai

# ── TypeScript SDK ─────────────────────────────────────────
mkdir -p $REPO/sdk/typescript/src

cat > $REPO/sdk/typescript/package.json <<'PKGJSON'
{
  "name": "@privatevault/sdk",
  "version": "0.1.0",
  "description": "PrivateVault AI Firewall SDK",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0"
  }
}
PKGJSON

cat > $REPO/sdk/typescript/tsconfig.json <<'TSJSON'
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "declaration": true,
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"]
}
TSJSON

cat > $REPO/sdk/typescript/src/index.ts <<'TSEOF'
import axios, { AxiosInstance } from "axios";

export type Decision = "ALLOW" | "REVIEW" | "BLOCK";

export interface EnforceResult {
  decision: Decision;
  reason: string;
  proof_hash: string;
  sandbox?: boolean;
}

export interface CheckPayload {
  agent_id: string;
  tool: string;
  args: Record<string, unknown>;
}

export class BlockedError extends Error {
  constructor(public reason: string, public proof_hash?: string) {
    super(`Blocked: ${reason} (proof=${proof_hash})`);
    this.name = "BlockedError";
  }
}

export class FirewallClient {
  private http: AxiosInstance;
  public sandbox: boolean;

  constructor(options: { apiKey: string; baseUrl?: string; sandbox?: boolean }) {
    this.sandbox = options.sandbox ?? false;
    const base = this.sandbox
      ? "http://localhost:8765"
      : (options.baseUrl ?? "https://api.privatevault.ai");

    this.http = axios.create({
      baseURL: base,
      timeout: 2000,
      headers: { "X-API-Key": options.apiKey, "Content-Type": "application/json" },
    });
  }

  async check(payload: CheckPayload): Promise<EnforceResult> {
    const { data } = await this.http.post<EnforceResult>("/v1/enforce", payload);
    return data;
  }

  async enforce<T>(
    payload: CheckPayload,
    fn: (args: Record<string, unknown>) => Promise<T>
  ): Promise<T> {
    const result = await this.check(payload);
    if (result.decision === "BLOCK") {
      throw new BlockedError(result.reason, result.proof_hash);
    }
    return fn(payload.args);
  }
}

export class AuditClient {
  private http: AxiosInstance;

  constructor(options: { apiKey: string; baseUrl?: string; sandbox?: boolean }) {
    const base = options.sandbox ? "http://localhost:8765" : (options.baseUrl ?? "https://api.privatevault.ai");
    this.http = axios.create({ baseURL: base, headers: { "X-API-Key": options.apiKey } });
  }

  async getLedger(): Promise<{ entries: unknown[]; count: number }> {
    const { data } = await this.http.get("/v1/ledger");
    return data;
  }
}
TSEOF

cat > $REPO/sdk/typescript/src/demo.ts <<'DEMOEOF'
import { FirewallClient, BlockedError } from "./index";

const pv = new FirewallClient({ apiKey: "sandbox-key", sandbox: true });

const tests = [
  { agent_id: "agent-1", tool: "read_file",  args: { path: "/data/report.csv" } },
  { agent_id: "agent-1", tool: "send_email", args: { to: "cfo@bank.com" } },
  { agent_id: "agent-1", tool: "delete_all", args: { table: "users" } },
];

(async () => {
  for (const payload of tests) {
    try {
      const r = await pv.check(payload);
      console.log(`[${r.decision.padEnd(6)}] ${payload.tool} → ${r.reason}`);
    } catch (e) {
      if (e instanceof BlockedError) console.log(`[BLOCKED] ${payload.tool} → ${e.reason}`);
      else throw e;
    }
  }
})();
DEMOEOF

echo "✅ TypeScript SDK created"

# ── Docker Compose ─────────────────────────────────────────
cat > $REPO/docker-compose.sandbox.yml <<'DCEOF'
version: "3.9"

services:

  sandbox:
    build:
      context: .
      dockerfile: Dockerfile.sandbox
    container_name: pv-sandbox
    ports:
      - "8765:8765"
    environment:
      - PV_MODE=sandbox
      - PV_LOG_LEVEL=info
    volumes:
      - sandbox-ledger:/app/ledger
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8765/health"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - pv-sandbox-net

  sandbox-ui:
    image: nginx:alpine
    container_name: pv-sandbox-ui
    ports:
      - "3000:80"
    volumes:
      - ./sandbox/ui:/usr/share/nginx/html:ro
    depends_on:
      - sandbox
    networks:
      - pv-sandbox-net

  redis:
    image: redis:7-alpine
    container_name: pv-sandbox-redis
    ports:
      - "6380:6379"
    networks:
      - pv-sandbox-net

volumes:
  sandbox-ledger:

networks:
  pv-sandbox-net:
    driver: bridge
DCEOF

cat > $REPO/Dockerfile.sandbox <<'DFEOF'
FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn httpx --break-system-packages 2>/dev/null || \
    pip install fastapi uvicorn httpx

COPY sandbox/sandbox_server.py .

EXPOSE 8765

CMD ["python", "sandbox_server.py"]
DFEOF

mkdir -p $REPO/sandbox/ui
cat > $REPO/sandbox/ui/index.html <<'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
  <title>PrivateVault Sandbox</title>
  <style>
    body { font-family: monospace; background: #0a0a0a; color: #00ff88; padding: 2rem; }
    h1 { color: #fff; } input, select { background: #111; color: #0f0; border: 1px solid #333; padding: 6px; margin: 4px; }
    button { background: #00ff88; color: #000; border: none; padding: 8px 16px; cursor: pointer; font-weight: bold; }
    pre { background: #111; padding: 1rem; border-left: 3px solid #00ff88; overflow-x: auto; }
    .BLOCK { color: #ff4444; } .ALLOW { color: #00ff88; } .REVIEW { color: #ffaa00; }
  </style>
</head>
<body>
  <h1>⚡ PrivateVault Sandbox</h1>
  <div>
    <input id="agent" value="agent-demo" placeholder="agent_id">
    <input id="tool" value="send_email" placeholder="tool name">
    <input id="args" value='{"to":"cfo@bank.com"}' placeholder='args JSON' style="width:300px">
    <button onclick="check()">Check</button>
  </div>
  <pre id="out">Result will appear here...</pre>
  <h3>Ledger</h3>
  <pre id="ledger">—</pre>
  <script>
    const API = "http://localhost:8765";
    async function check() {
      const r = await fetch(`${API}/v1/enforce`, {
        method: "POST", headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ agent_id: document.getElementById("agent").value,
          tool: document.getElementById("tool").value,
          args: JSON.parse(document.getElementById("args").value) })
      });
      const d = await r.json();
      const el = document.getElementById("out");
      el.textContent = JSON.stringify(d, null, 2);
      el.className = d.decision;
      loadLedger();
    }
    async function loadLedger() {
      const r = await fetch(`${API}/v1/ledger`);
      const d = await r.json();
      document.getElementById("ledger").textContent = JSON.stringify(d.entries.slice(-5), null, 2);
    }
    loadLedger();
  </script>
</body>
</html>
HTMLEOF

echo "✅ Docker Compose sandbox created"
echo ""
echo "── COMMANDS ─────────────────────────────────────────"
echo "Start sandbox stack:   docker compose -f docker-compose.sandbox.yml up -d"
echo "View logs:             docker compose -f docker-compose.sandbox.yml logs -f sandbox"
echo "Sandbox UI:            http://localhost:3000"
echo "API health:            http://localhost:8765/health"
echo "Ledger:                http://localhost:8765/v1/ledger"
echo ""
echo "TS SDK build:          cd sdk/typescript && npm install && npm run build"
echo "TS demo:               npx ts-node src/demo.ts"
echo "────────────────────────────────────────────────────"
