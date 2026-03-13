import os
import traceback
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ PrivateVault backend is live"

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 10000))  # Render uses this dynamic port
        print(f"🚀 Starting Flask on port {port} ...")
        app.run(host="0.0.0.0", port=port)
    except Exception:
        traceback.print_exc()

