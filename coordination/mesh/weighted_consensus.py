def compute_weighted_consensus(agent_votes):
    total_weight = 0
    positive_weight = 0

    for agent in agent_votes:
        weight = agent.get("weight", 0)
        vote = agent.get("vote", False)

        total_weight += weight
        if vote:
            positive_weight += weight

    if total_weight == 0:
        return {"allowed": False, "reason": "No valid weights"}

    score = positive_weight / total_weight

    return {
        "allowed": score >= 0.5,
        "score": score,
        "total_weight": total_weight
    }


def main():
    print("🚀 Running Weighted Consensus...")

    agent_votes = [
        {"agent_id": "agent_1", "vote": True, "weight": 0.8},
        {"agent_id": "agent_2", "vote": True, "weight": 0.6},
        {"agent_id": "agent_3", "vote": False, "weight": 0.4},
    ]

    result = compute_weighted_consensus(agent_votes)

    print("✅ Result:")
    print(result)


if __name__ == "__main__":
    main()
