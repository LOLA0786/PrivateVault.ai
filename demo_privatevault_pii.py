from security.pii.runtime_governance import govern_response

llm_response = {
    "choices": [
        {
            "message": {
                "content": """
Customer Records

Rahul Sharma
Email: rahul@gmail.com
Phone: 9876543210
PAN: ABCDE1234F

Priya Singh
Email: priya@gmail.com
Phone: 9988776655
PAN: FGHIJ5678K
"""
            }
        }
    ]
}

result = govern_response(llm_response)

print("=" * 50)
print("PRIVATEVAULT RUNTIME")
print("=" * 50)

print("PII DETECTED:", result["count"])

print("\nTYPES FOUND:")

for item in result["findings"]:
    print("-", item["type"])

print("\nSANITIZED OUTPUT:\n")

print(
    result["response"]["choices"][0]
    ["message"]["content"]
)
