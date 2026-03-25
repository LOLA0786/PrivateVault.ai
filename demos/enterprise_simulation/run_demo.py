from pv_runtime.entrypoint import execute

SCENARIOS = [
    {"action": "transfer_funds", "amount": 5000},
    {"action": "transfer_funds", "amount": 50000},
    {"action": "transfer_funds", "amount": 1000000, "override": True},
    {"action": "get_weather", "location": "Mumbai"},
]

for i, scenario in enumerate(SCENARIOS):
    print(f"\n=== SCENARIO {i+1} ===")
    result = execute(scenario, "agent_1")
    print(result)
