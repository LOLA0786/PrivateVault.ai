from pv_runtime.entrypoint import execute

result = execute(
    {
        "action":"get_weather"
    },
    "test_agent"
)

print(result.keys())

print(
    result.get(
        "adversarial"
    )
)
