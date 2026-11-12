import pytest

from parser import ParseError, parse_command

def test_command_with_arguments():
    assert parse_command('add_numbers {"a": 2, "b": 5}') == ("add_numbers", {"a": 2, "b": 5})

def test_command_without_arguments():
    assert parse_command("get_date_time") == ("get_date_time", {})

def test_extra_whitespace_is_ignored():
    assert parse_command('  add_numbers   {"a": 2}  ') == ("add_numbers", {"a": 2})


@pytest.mark.parametrize("line", ["", "   "])
def test_empty_command(line):
    with pytest.raises(ParseError):
        parse_command(line)


def test_invalid_json():
    with pytest.raises(ParseError):
        parse_command("add_numbers {a: 2}")


@pytest.mark.parametrize("raw", ["[1, 2]", "5"])
def test_arguments_must_be_object(raw):
    with pytest.raises(ParseError):
        parse_command(f"add_numbers {raw}")