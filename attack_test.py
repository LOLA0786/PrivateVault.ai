print("=== BYPASS TEST ===")

try:
    import tools   # or whatever your raw module name is

    print("[ATTACK] Direct call: transfer_funds(300000)")
    tools.transfer_funds(300000)

    print("❌ BYPASS SUCCESS — SYSTEM IS NOT SAFE")

except Exception as e:
    print("✅ BLOCKED:", e)
