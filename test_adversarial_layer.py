from pv_runtime.adversarial.runtime_hook import (
    evaluate_adversarial_risk
)

cases = [

    {
        "name": "normal",
        "history": ["show weather in mumbai"],
        "agents": ["agent1"]
    },

    {
        "name": "context_stitching",
        "history": [
            "previous step",
            "combine earlier results",
            "continue process"
        ],
        "agents": ["agent1"]
    },

    {
        "name": "collusion",
        "history": ["normal"],
        "agents": ["a","b","a","b"]
    }

]

for c in cases:

    result = evaluate_adversarial_risk(
        history=c["history"],
        agent_chain=c["agents"]
    )

    print("\n====", c["name"], "====")
    print(result)

