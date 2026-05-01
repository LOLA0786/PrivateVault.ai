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
