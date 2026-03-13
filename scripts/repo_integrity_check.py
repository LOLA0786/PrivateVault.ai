import os
import py_compile

errors = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                py_compile.compile(path, doraise=True)
            except Exception as e:
                errors.append((path, str(e)))

if errors:
    print("FAILED FILES:")
    for e in errors:
        print(e)
    exit(1)

print("REPO INTEGRITY OK")
