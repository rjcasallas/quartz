#!/usr/bin/env bash

# Get script path (Bash or Zsh)
if [ -n "$BASH_VERSION" ]; then
    SCRIPT_PATH="${BASH_SOURCE[0]}"
elif [ -n "$ZSH_VERSION" ]; then
    SCRIPT_PATH="${(%):-%x}"
else
    echo "Unsupported shell. Please use Bash or Zsh."
fi

# Get the absolute directory path
QUARTZ_DIR="$(cd -P "$(dirname -- "$SCRIPT_PATH")" && pwd)"
echo "Quartz dir: $QUARTZ_DIR"

# Python path
export PYTHONPATH=${QUARTZ_DIR}/common/python:${QUARTZ_DIR}/examples/python
