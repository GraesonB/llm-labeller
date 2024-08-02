import pytest

@pytest.fixture
def sample_data():
    return {"key1": "value1", "key2": "value2"}

def test_sample_data(sample_data):
    assert sample_data["key1"] == "value1"
    assert sample_data["key2"] == "value2"
