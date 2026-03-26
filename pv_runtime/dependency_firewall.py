import os
import socket
import builtins
import requests
import subprocess

# -------------------------
# CONFIG
# -------------------------
BLOCKED_PATHS = [
    os.path.expanduser("~/.ssh"),
    os.path.expanduser("~/.aws"),
    os.path.expanduser("~/.config/gcloud"),
    os.path.expanduser("~/.kube"),
]

SENSITIVE_ENV_KEYS = [
    "AWS_SECRET_ACCESS_KEY",
    "AWS_ACCESS_KEY_ID",
    "OPENAI_API_KEY",
    "GOOGLE_API_KEY",
    "AZURE_API_KEY"
]

ALLOWED_DOMAINS = ["api.openai.com", "yourcompany.com"]

# -------------------------
# FILE ACCESS CONTROL
# -------------------------
_original_open = builtins.open

def secure_open(file, *args, **kwargs):
    for path in BLOCKED_PATHS:
        if file.startswith(path):
            raise PermissionError(f"[PV] Blocked file access: {file}")
    return _original_open(file, *args, **kwargs)

builtins.open = secure_open

# -------------------------
# ENV ACCESS CONTROL
# -------------------------
_original_getenv = os.getenv

def secure_getenv(key, default=None):
    if key in SENSITIVE_ENV_KEYS:
        raise PermissionError(f"[PV] Blocked env access: {key}")
    return _original_getenv(key, default)

os.getenv = secure_getenv

# -------------------------
# NETWORK CONTROL (requests)
# -------------------------
_original_post = requests.post

def secure_post(url, *args, **kwargs):
    try:
        domain = url.split("/")[2]
    except:
        domain = ""
    if domain not in ALLOWED_DOMAINS:
        raise PermissionError(f"[PV] Blocked HTTP exfiltration: {domain}")
    return _original_post(url, *args, **kwargs)

requests.post = secure_post

# -------------------------
# SUBPROCESS BLOCK
# -------------------------
_original_popen = subprocess.Popen

def secure_popen(*args, **kwargs):
    raise PermissionError("[PV] Blocked subprocess execution")

subprocess.Popen = secure_popen
subprocess.call = secure_popen
subprocess.run = secure_popen

# -------------------------
# OS COMMAND BLOCK
# -------------------------
def blocked_system(*args, **kwargs):
    raise PermissionError("[PV] Blocked os.system execution")

os.system = blocked_system

# -------------------------
# SOCKET BLOCK
# -------------------------
_original_socket = socket.socket

class SecureSocket(socket.socket):
    def connect(self, *args, **kwargs):
        raise PermissionError("[PV] Blocked raw socket connection")

socket.socket = SecureSocket

print("[PrivateVault] HARDENED FIREWALL ACTIVE")
