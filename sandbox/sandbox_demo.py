"""
Quick demo: SDK talking to sandbox
Run sandbox_server.py first, then this.
"""
import sys
sys.path.insert(0, "../sdk/python")
from privatevault import FirewallClient
from privatevault.firewall.client import BlockedError

pv = FirewallClient(api_key="sandbox-key", sandbox=True)

tests = [
    ("agent-1", "read_file",    {"path": "/data/report.csv"}),
    ("agent-1", "send_email",   {"to": "cfo@bank.com", "body": "Q3 results"}),
    ("agent-1", "delete_all",   {"table": "users"}),
]

for agent, tool, args in tests:
    try:
        result = pv.check(agent, tool, args)
        print(f"[{result['decision']:6}] {tool} → {result['reason']}")
    except BlockedError as e:
        print(f"[BLOCKED] {tool} → {e.reason}")
