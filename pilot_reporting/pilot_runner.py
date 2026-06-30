import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(BASE_DIR)

from findings_engine import FindingsEngine, save_findings
from executive_report import build_report, save_report

OUTPUT_DIR = os.path.join(ROOT_DIR, "pilot_output")
INPUT_FILE = os.path.join(OUTPUT_DIR, "decision_records.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_records():

    if not os.path.exists(INPUT_FILE):
        print(f"Missing: {INPUT_FILE}")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)

def main():

    records = load_records()

    engine = FindingsEngine()

    findings = engine.analyze(records)

    save_findings(
        findings,
        os.path.join(OUTPUT_DIR, "findings.json")
    )

    report = build_report(findings)

    save_report(
        report,
        os.path.join(OUTPUT_DIR, "executive_report.md")
    )

    print("Generated:")
    print(os.path.join(OUTPUT_DIR, "findings.json"))
    print(os.path.join(OUTPUT_DIR, "executive_report.md"))

if __name__ == "__main__":
    main()
