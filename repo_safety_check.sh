#!/bin/bash

echo "Running integrity checks..."

python -m compileall privatevault > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Python compilation failed"
    exit 1
fi

pytest -q
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✅ Repo safe to push"
