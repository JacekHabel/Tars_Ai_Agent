"""Turns a text command into a tool name and it's atguments."""

import json
from typing import Any

class ParseError(Exception):
    """Raised when a command line cannot be understood."""

def parse_command(line: str) -> tuple[str, dict[str, Any]]:
    """Parse 'tool_name {json arguments}' into (tool_name, arguments)."""
    line = line.strip()
    if not line:
        raise ParseError("Empty command.")

    name, _, raw_args = line.partition(" ")
    raw_args = raw_args.strip()
    if not raw_args:
        return name, {}

    try:
        args = json.loads(raw_args)
    except json.JSONDecodeError as e:
        raise ParseError(f"Invalid JSON arguments: {e.msg}")

    if not isinstance(args, dict):
        raise ParseError("Arguments must be a JSON object, e.g. {\"a\": 1}.")
    return name, args
    