import argparse
import json
import sys

from pv_runtime.proven_execute import proven_execute
from verify import verify_proof


def clean_json_output(data):
    json.dump(data, sys.stdout, indent=2)
    print()


def run_cmd(args):
    with open(args.input) as f:
        input_data = json.load(f)

    result = proven_execute(raw_intent=input_data, agent_id="pv-cli")

    # 🔥 force clean JSON output only
    clean_json_output(result)


def load_clean_json(path):
    with open(path) as f:
        content = f.read()

    # 🔥 remove any non-JSON lines (like [ASYNC])
    lines = content.splitlines()
    clean_lines = [l for l in lines if not l.strip().startswith("[")]

    return json.loads("\n".join(clean_lines))


def receipt_cmd(args):
    data = load_clean_json(args.input)
    clean_json_output(data.get("receipt", {}))


def verify_cmd(args):
    data = load_clean_json(args.input)
    proof = data.get("proof", {})
    result = verify_proof(proof)
    clean_json_output(result)


def main():
    parser = argparse.ArgumentParser("pvcli")
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run")
    run_parser.add_argument("input")
    run_parser.set_defaults(func=run_cmd)

    receipt_parser = sub.add_parser("receipt")
    receipt_parser.add_argument("input")
    receipt_parser.set_defaults(func=receipt_cmd)

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("input")
    verify_parser.set_defaults(func=verify_cmd)

    # economics sub-command
    econ_p = sub.add_parser("economics", help="Agent economics — cost, waste, ROI")
    econ_sub = econ_p.add_subparsers(dest="econ_cmd")

    ep_sum = econ_sub.add_parser("summary", help="Economics summary for an agent")
    ep_sum.add_argument("agent")
    ep_sum.add_argument("--days", type=int, default=7)

    ep_wf = econ_sub.add_parser("workflow", help="Cost breakdown for a workflow")
    ep_wf.add_argument("workflow")
    ep_wf.add_argument("--days", type=int, default=7)

    ep_rec = econ_sub.add_parser("recent", help="Tail recent executions")
    ep_rec.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    elif args.command == "economics":
        if not hasattr(args, "econ_cmd") or args.econ_cmd is None:
            econ_p.print_help()
        elif args.econ_cmd == "summary":
            economics_summary_cmd(args)
        elif args.econ_cmd == "workflow":
            economics_workflow_cmd(args)
        elif args.econ_cmd == "recent":
            economics_recent_cmd(args)
    else:
        parser.print_help()


#if __name__ == "__main__":
#    main()


# ─────────────────────────────────────────────
# pvcli economics (argparse-native)
# ─────────────────────────────────────────────


def economics_summary_cmd(args):
    from pv_economics.storage.economics_store import EconomicsStore
    data = EconomicsStore().get_agent_summary(args.agent, days=args.days)
    if data.get("runs", 0) == 0:
        print(f"No data for agent '{args.agent}' in last {args.days} days.")
        return
    success_pct = round(data["success_rate"] * 100, 1)
    print(f"\n{'─'*48}")
    print(f"  Economics: {args.agent}  ({args.days}d window)")
    print(f"{'─'*48}")
    print(f"  Runs            {data['runs']:>10,}")
    print(f"  Total cost      ${data['total_cost_usd']:>10.4f}")
    print(f"  Avg cost/run    ${data['avg_cost_usd']:>10.6f}")
    print(f"  Success rate    {success_pct:>9.1f}%")
    print(f"  Avg waste score {data['avg_waste']:>10.1f}/100")
    print(f"  Avg ROI ratio   {data['avg_roi']:>10.2f}x")
    print(f"  Avg econ score  {data['avg_econ_score']:>10.1f}/100")
    print(f"  Avg latency     {data['avg_latency_ms']:>9.0f}ms")
    print(f"  Total tokens    {data['total_tokens']:>10,}")
    print(f"{'─'*48}\n")


def economics_workflow_cmd(args):
    from pv_economics.storage.economics_store import EconomicsStore
    data = EconomicsStore().get_workflow_summary(args.workflow, days=args.days)
    agents = data.get("agents", [])
    if not agents:
        print(f"No data for workflow '{args.workflow}'.")
        return
    print(f"\n{'─'*60}")
    print(f"  Workflow: {args.workflow}  ({args.days}d)")
    print(f"{'─'*60}")
    print(f"  {'Agent':<30} {'Runs':>5} {'Cost':>9} {'Waste':>6} {'Success':>8}")
    print(f"  {'─'*30} {'─'*5} {'─'*9} {'─'*6} {'─'*8}")
    for a in sorted(agents, key=lambda x: x["cost_usd"], reverse=True):
        print(
            f"  {a['agent']:<30} {a['runs']:>5,} "
            f"${a['cost_usd']:>8.4f} {a['avg_waste']:>5.1f}  "
            f"{a['success_rate']*100:>6.1f}%"
        )
    print(f"{'─'*60}\n")


def economics_recent_cmd(args):
    from pv_economics.storage.economics_store import EconomicsStore
    rows = EconomicsStore().get_recent(limit=args.limit)
    if not rows:
        print("No executions recorded yet.")
        return
    divider = chr(9472) * 80
    header  = chr(9472) * 80
    print()
    print("  " + divider)
    print("  {:<24} {:<22} {:>5} {:>8} {:>6} {:>6}".format(
        "Timestamp", "Agent", "Grade", "Cost", "Waste", "ROI"
    ))
    print("  " + divider)
    for r in rows:
        ts = r["ts"][:19].replace("T", " ")
        print("  {:<24} {:<22} {:>5} ${:>7.5f} {:>5.1f}  {:>5.1f}x".format(
            ts,
            r["agent"],
            r["econ_grade"] or "-",
            r["cost_usd"],
            r["waste_score"],
            r["roi_score"],
        ))
    print("  " + divider)
    print()

if __name__ == "__main__":
    main()
