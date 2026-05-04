from pv_core.simulation.simulator import run
from pv_cost_layer.integration.execute_with_controls import execute_with_controls


def main():
    # sample intent (adjust if needed)
    intent = {
        "provider": "gpt",
        "input_tokens": 1000,
        "output_tokens": 500,
        "risk_score": 0.1,
        "action": {"recipient": "vendor_x"}
    }

    result = execute_with_controls(run, intent)
    print(result)


if __name__ == "__main__":
    main()
