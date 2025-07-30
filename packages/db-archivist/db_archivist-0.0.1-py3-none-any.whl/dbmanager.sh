#!/bin/bash
# Convenience script for running dbmanager with uvx
# Usage: ./dbmanager.sh <command> [options]

# Change to the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the command with uvx
uvx --from . dbmanager "$@" 