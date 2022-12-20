import pytest

from .brackets_definitions import BracketsDefinition
from .matching_brackets_validator import MatchingBracketValidator


@pytest.mark.parametrize(
    "text_input, expected_output",
    [
        ("", True),
        ("()", True),
        ("()()", True),
        ("(())", True),
        ("(", False),
        (")", False),
        (")(", False),
    ],
)
def test_should_validate_parentheses(text_input, expected_output):
    object_under_test = MatchingBracketValidator(
        bracket_definitions=[
            BracketsDefinition(opening="(", closing=")"),
        ],
    )
    assert object_under_test.do_brackets_match(txt=text_input) is expected_output


@pytest.mark.parametrize(
    "text_input, expected_output",
    [
        ("", True),
        ("[]", True),
        ("[][]", True),
        ("[[]]", True),
        ("[", False),
        ("]", False),
        ("][", False),
    ],
)
def test_should_validate_square_brackets(text_input, expected_output):
    object_under_test = MatchingBracketValidator(
        bracket_definitions=[
            BracketsDefinition(opening="[", closing="]"),
        ],
    )
    assert object_under_test.do_brackets_match(txt=text_input) is expected_output


@pytest.mark.parametrize(
    "text_input, expected_output",
    [
        ("", True),
        ("{}", True),
        ("{}{}", True),
        ("{{}}", True),
        ("}", False),
        ("}", False),
        ("}{", False),
    ],
)
def test_should_validate_curly_braces(text_input, expected_output):
    object_under_test = MatchingBracketValidator(
        bracket_definitions=[
            BracketsDefinition(opening="{", closing="}"),
        ],
    )
    assert object_under_test.do_brackets_match(txt=text_input) is expected_output


@pytest.mark.parametrize(
    "text_input, expected_output",
    [
        ("[()]", True),
        ("([])", True),
        ("()[]", True),
        ("([)]", False),
        ("[(])", False),
    ],
)
def test_should_validate_multiple_types_of_brackets(text_input, expected_output):
    object_under_test = MatchingBracketValidator(
        bracket_definitions=[
            BracketsDefinition(opening="(", closing=")"),
            BracketsDefinition(opening="[", closing="]"),
            BracketsDefinition(opening="{", closing="}"),
        ],
    )
    assert object_under_test.do_brackets_match(txt=text_input) is expected_output
