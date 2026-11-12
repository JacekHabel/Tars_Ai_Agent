from datetime import datetime

import pytest

from registry import ToolError
from tools import build_registry

@pytest.fixture
def registry():
    return build_registry()

def test_get_date_time_return_valid_iso_datetime(registry):
    result = registry.execute("get_date_time",{})
    datetime.fromisoformat(result)

def test_add_numbers(registry):
    assert registry.execute("add_numbers", {"a": 2, "b": 3}) == 5


def test_add_numbers_accepts_floats(registry):
    assert registry.execute("add_numbers", {"a": 0.5, "b": 0.25}) == 0.75

def test_get_date_time_rejects_arguments(registry):
    with pytest.raises(ToolError):
        registry.execute("get_date_time", {"banana": True})


def test_both_tools_are_registered(registry):
    with pytest.raises(ValueError):
        # registering the same name twice must fail, so both exist
        from registry import Tool
        registry.register(Tool("get_time", "x", {}, lambda: None))
        registry.register(Tool("add_numbers", "x", {}, lambda: None))