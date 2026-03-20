from tool_authorization import authorize_tool_call

tests = [
    ("viewer_003", "weather_api", {"action": "get weather data"}),
    ("viewer_003", "payment_api", {"action": "transfer money to vendor"}),
    ("viewer_003", "db", {"action": "delete user table"})
]

for user, tool, params in tests:
    print("\n---")
    res = authorize_tool_call(user, tool, params)
    print(res)
