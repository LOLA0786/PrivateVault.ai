def compute_ppo_reward(outcome):
    reward = 10 if getattr(outcome,'success',True) else -20
    print(f"🏆 PPO reward computed = {reward} | outcome → future agent cognition")
