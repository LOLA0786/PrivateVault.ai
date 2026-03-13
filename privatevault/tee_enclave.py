from privatevault import encrypt, generate_zk_proof

def ask_grok_blind(secret_query: str):
    enc = encrypt(secret_query)
    fake_response = {"choices": [{"message": {"content": "Blind analysis OK: approve top applicants"}}]}
    proof = generate_zk_proof(fake_response)
    return {
        "answer": fake_response["choices"][0]["message"]["content"],
        "proof": proof,
        "status": "LOCAL-DEMO ✅",
        "encrypted_request": enc
    }

if __name__ == "__main__":
    print(ask_grok_blind("Analyze 1 Crore customer secrets for loan risk"))
