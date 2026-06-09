from pv_runtime_v2.economics.coordination_optimizer import (
    CoordinationOptimizer,
)


def scenario(
    agents,
    gain,
    impact,
    latency,
):

    optimizer = (
        CoordinationOptimizer()
    )

    expand = (
        optimizer.should_expand(
            current_agents=agents,
            expected_confidence_gain=gain,
            impact=impact,
            latency_ms=latency,
        )
    )

    print(
        f"agents={agents} "
        f"gain={gain} "
        f"impact={impact} "
        f"latency={latency} "
        f"expand={expand}"
    )


if __name__ == "__main__":

    scenario(
        5,
        0.20,
        100,
        1,
    )

    scenario(
        50,
        0.05,
        100,
        1,
    )

    scenario(
        500,
        0.01,
        100,
        1,
    )

    scenario(
        5000,
        0.001,
        100,
        1,
    )
