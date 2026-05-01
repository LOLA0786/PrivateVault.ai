import os
import requests
import json
import uuid

HYDRA_API_KEY = os.getenv("HYDRADB_API_KEY")
BASE_URL = "https://api.hydradb.com"

class HydraClient:
    def __init__(self, tenant_id="privatevault-demo", sub_tenant_id="demo"):
        self.tenant_id = tenant_id
        self.sub_tenant_id = sub_tenant_id

    def ingest_policy(self, content_text):
        headers = {
            "Authorization": f"Bearer {HYDRA_API_KEY}"
        }

        # 🔥 FULL STRUCTURE REQUIRED BY HYDRA
        app_knowledge = json.dumps([
            {
                "id": str(uuid.uuid4()),
                "tenant_id": self.tenant_id,
                "sub_tenant_id": self.sub_tenant_id,
                "content": {
                    "text": content_text
                },
                "metadata": {
                    "type": "policy",
                    "risk": "high"
                }
            }
        ])

        data = {
            "tenant_id": self.tenant_id,
            "sub_tenant_id": self.sub_tenant_id,
            "app_knowledge": app_knowledge
        }

        response = requests.post(
            f"{BASE_URL}/ingestion/upload_knowledge",
            headers=headers,
            data=data
        )

        return response.text

    def query(self, question):
        headers = {
            "Authorization": f"Bearer {HYDRA_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "question": question,
            "session_id": "pv-demo",
            "tenant_id": self.tenant_id,
            "sub_tenant_id": self.sub_tenant_id
        }

        response = requests.post(
            f"{BASE_URL}/search/qna",
            headers=headers,
            json=payload
        )

        return response.json()


if __name__ == "__main__":
    client = HydraClient()

    print(">> Uploading policy...")
    upload_res = client.ingest_policy(
        "Maximum transaction limit is 250000 INR. Any transaction above this must be blocked."
    )
    print(upload_res)

    print("\n>> Querying context...")
    query_res = client.query("What is the transaction limit?")
    print(query_res)
