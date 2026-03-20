from agent_executor_firewalled import execute_action

tests = [
    "get weather data",
    "scrape website",
    "transfer money to vendor",
    "delete database"
]

for t in tests:
    print("\n=== ACTION:", t)
    print(execute_action(t))
