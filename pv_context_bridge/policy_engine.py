import json

def extract_limit(hydra_response):
    try:
        chunks = hydra_response.get("chunks", [])
        if not chunks:
            return None

        raw = chunks[0]["chunk_content"]
        parsed = json.loads(raw)

        text = parsed["content"]["text"]

        # simple extraction (can upgrade later)
        if "250000" in text:
            return 250000

    except Exception as e:
        print("Parse error:", e)

    return None
