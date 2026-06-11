from security.pii.redactor import redact

sample = """
Rahul Sharma
PAN ABCDE1234F
Aadhaar 123456789012
Email rahul@gmail.com
Phone 9876543210
"""

output, findings = redact(sample)

print("OUTPUT:")
print(output)

print("\nFINDINGS:")
print(findings)
