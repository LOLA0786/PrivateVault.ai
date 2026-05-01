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
    sub = parser.add_subparsers()

    run_parser = sub.add_parser("run")
    run_parser.add_argument("input")
    run_parser.set_defaults(func=run_cmd)

    receipt_parser = sub.add_parser("receipt")
    receipt_parser.add_argument("input")
    receipt_parser.set_defaults(func=receipt_cmd)

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("input")
    verify_parser.set_defaults(func=verify_cmd)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
