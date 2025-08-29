from fastapi.testclient import TestClient
from app.main import app  # ensure app/__init__.py exists

client = TestClient(app)

def post(data):
    return client.post("/bfhl", json={"data": data})

def test_example_a():
    # Example A from prompt
    r = post(["a", "1", "334", "4", "R", "$"])
    assert r.status_code == 200
    j = r.json()
    assert j["is_success"] is True
    assert j["odd_numbers"] == ["1"]
    assert j["even_numbers"] == ["334", "4"]
    assert j["alphabets"] == ["A", "R"]
    assert j["special_characters"] == ["$"]
    assert j["sum"] == "339"
    assert j["concat_string"] == "Ra"

def test_example_b():
    r = post(["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"])
    assert r.status_code == 200
    j = r.json()
    assert j["is_success"] is True
    assert j["odd_numbers"] == ["5"]
    assert j["even_numbers"] == ["2", "4", "92"]
    assert j["alphabets"] == ["A", "Y", "B"]
    assert j["special_characters"] == ["&", "-", "*"]
    assert j["sum"] == "103"
    assert j["concat_string"] == "ByA"

def test_example_c():
    r = post(["A", "ABcD", "DOE"])
    assert r.status_code == 200
    j = r.json()
    assert j["is_success"] is True
    assert j["odd_numbers"] == []
    assert j["even_numbers"] == []
    assert j["alphabets"] == ["A", "ABCD", "DOE"]
    assert j["special_characters"] == []
    assert j["sum"] == "0"
    assert j["concat_string"] == "EoDdCbAa"

def test_mixed_alnum_is_special():
    # includes a space token; our server strips -> "" and treats as special
    r = post(["abc123", "-42", "+9", "foo", "bar!", " "])
    j = r.json()
    assert j["even_numbers"] == ["-42"]
    assert j["odd_numbers"] == ["+9"]
    assert j["alphabets"] == ["FOO"]
    # "abc123", "bar!", and "" (space => stripped) should be special
    assert j["special_characters"] == ["abc123", "bar!", ""]
    assert j["sum"] == str(-42 + 9)
