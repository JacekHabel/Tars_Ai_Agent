import pytest

from registry import Tool, ToolError, ToolRegistry

ADD_SCHEMA = {
    "type": "object",
    "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
    "required": ["a", "b"],
    "additionalProperties": False
}

def add_numbers(a, b):
    return a + b

def crash():
    return 1 / 0

@pytest.fixture
def registry():
    reg = ToolRegistry()
    reg.register(Tool("add_numbers", "Add two numbers.", ADD_SCHEMA, add_numbers))
    return reg

def test_valid_call(registry):
    assert registry.execute("add_numbers", {"a": 2, "b": 3}) == 5

def test_unkown_tool(registry):
    with pytest.raises(ToolError):
        registry.execute("rm_rf", {})

def test_missing_argument(registry):
    with pytest.raises(ToolError):
        registry.execute("add_numbers", {"a": 1})


def test_wrong_type(registry):
    with pytest.raises(ToolError):
        registry.execute("add_numbers", {"a": "x", "b": 1})


def test_extra_argument_rejected(registry):
    with pytest.raises(ToolError):
        registry.execute("add_numbers", {"a": 1, "b": 2, "evil": True})


def test_duplicate_registration(registry):
    with pytest.raises(ValueError):
        registry.register(Tool("add_numbers", "Again.", ADD_SCHEMA, add_numbers))


def test_tool_crash_becomes_tool_error(registry):
    registry.register(Tool("crash", "Always fails.", {"type": "object", "properties": {}}, crash))
    with pytest.raises(ToolError):
        registry.execute("crash", {})