import json

from app import clean_json_text, parse_answer


def test_parse_wrapped_answer():
    assert parse_answer('{"answer":{"state":"Assam"}}') == {"state": "Assam"}


def test_parse_scalar_answer():
    assert parse_answer("```json\n{\"answer\":42}\n```") == 42


def test_clean_output_is_json_serializable():
    value = parse_answer('{"answer":[1,2,3]}')
    assert json.dumps(value) == "[1, 2, 3]"
