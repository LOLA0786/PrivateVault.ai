#!/bin/bash
set -e

ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519 -N ""
echo "✅ SSH key generated"
echo "----- COPY THIS -----"
cat ~/.ssh/id_ed25519.pub
echo "---------------------"
