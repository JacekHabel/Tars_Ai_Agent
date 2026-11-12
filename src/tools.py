"""Tools avaliable for agent"""

from datetime import datetime

from registry import ToolRegistry, Tool

def get_date_time() -> str:
    """Return the current local date and time in ISO 8601 format."""
    return datetime.now().isoformat(timespec="seconds")

def add_numbers(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def build_registry() -> ToolRegistry:
    """Create a registry with all available tools."""
    registry = ToolRegistry()
    
    registry.register(Tool(
        name="get_date_time",
        description="Get the current local date and time.",
        parameters={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        func=get_date_time,
    ))

    registry.register(Tool(
        name="add_numbers",
        description="Add two numbers.",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
            "additionalProperties": False,
        },
        func=add_numbers,
    ))
    return registry