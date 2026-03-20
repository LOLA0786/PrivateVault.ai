from agent_executor_firewalled import execute_action

tests = [
    "fetch user profile",
    "transfer money to external account",
    "delete production database"
]

for t in tests:
    print("\n=== ACTION:", t)
    res = execute_action(t)
    print("RESULT:", res)
