from security.pii.runtime_governance import govern_response

sample = {
    "choices": [{
        "message": {
            "content": """
Rahul Sharma
Email rahul@gmail.com
Phone 9876543210
PAN ABCDE1234F
"""
        }
    }]
}

result = govern_response(sample)

print("DECISION:", result["decision"])
print("REASON:", result["reason"])
print("COUNT:", result["count"])
