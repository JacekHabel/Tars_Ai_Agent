"""Tool registry and execution management."""

from dataclasses import dataclass
from typing import Any, Callable

from jsonschema import ValidationError, validate

class ToolError(Exception):
    """Raised when a tool operation fails."""

@dataclass(frozen=True)
class Tool:
    """Represents a single executable tool."""

    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., Any]
    reguires_confirmation: bool = False

class ToolRegistry:
    """Stores tools and executes them safely."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Duplicate tool: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise ToolError(f"Unknown tool: '{name}'. Available: {sorted(self._tools)}")
        return self._tools[name]

    def execute(self, name: str, args: dict[str, Any]) -> Any:
        tool = self.get(name)
        try:
            validate(instance=args, schema=tool.parameters)
        except ValidationError as e:
            raise ToolError(f"Invalid arguments for '{name}': {e.message}")
        try:
            return tool.func(**args)
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Tool '{name}' failed: {e}")    
    