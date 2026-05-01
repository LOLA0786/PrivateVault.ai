print("=== DEEP BYPASS TEST ===")

# Test 1: direct gateway import misuse
try:
    import gateway
    print("[ATTACK] Trying gateway internal access")

    if hasattr(gateway, "_tools"):
        gateway._tools.transfer_funds(300000)
        print("❌ BYPASS via _tools")
    else:
        print("✅ _tools not exposed")

except Exception as e:
    print("✅ BLOCKED:", e)


# Test 2: try grabbing function reference
try:
    from gateway import transfer_funds
    print("[ATTACK] Direct function import")

    transfer_funds(300000)
    print("❌ BYPASS via direct import")

except Exception as e:
    print("✅ BLOCKED:", e)
