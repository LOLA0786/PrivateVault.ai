from security.agent_firewall.firewall import firewall_check

tests = [
    "get weather data",
    "transfer money to account",
    "delete database",
    "scrape website data",
    "normal user query"
]

for t in tests:
    print("\n---")
    print(firewall_check(t))
