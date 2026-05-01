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
