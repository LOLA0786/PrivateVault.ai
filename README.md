# PrivateVault: Zero-Trust Runtime for Dependencies

A single `pip install` can expose:
- AWS credentials
- API keys
- SSH keys
- CI/CD secrets

## Demo

### Without protection
python fake_litellm_install.py

→ Secrets accessed and exfiltration succeeds

### With PrivateVault
python run_secure.py

→ All attack paths blocked:
- file access
- env access
- HTTP exfiltration
- subprocess (curl)
- os.system
- raw sockets

## Secure Install
./pv_secure_pip.sh litellm

→ isolates environment and prevents credential exposure

## Key Idea
Assume dependencies are compromised.
Enforce zero-trust execution at runtime and install-time.
