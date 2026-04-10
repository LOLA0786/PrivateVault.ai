import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: pv-cli [init|check-risk]")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        print("✅ PrivateVault initialized")

    elif cmd == "check-risk":
        print("🔍 Analyzing decision...")
        print("⚠️ Risk detected: HIGH")
        print("🛑 Action blocked")

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
