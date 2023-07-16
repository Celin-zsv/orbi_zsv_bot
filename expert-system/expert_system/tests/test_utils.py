import time

import pytest
from expert_system.utils import TextPreprocessor, find_closest_request, timeit


def test_timeit_decorator(capfd):
    """timeit decorator should return correct time."""

    @timeit
    def test_function():
        time.sleep(1)

    test_function()
    out, _ = capfd.readouterr()
    assert "Elapsed time for test_function: " in out
    assert " sec." in out
    elapsed_time = float(out.split(": ")[-1].split(" sec.")[0])
    assert 1.1 >= elapsed_time >= 1.0


def test_text_preprocessor():
    """Test TextPreprocessor class."""
    input_text = "Это простой текст, он !2@ содержит стоп-слова и пунктуацию какие как!"
    preprocessor = TextPreprocessor(input_text)
    preprocessor._tokenize()
    assert preprocessor.tokens == [
        "это",
        "простой",
        "текст",
        ",",
        "он",
        "!",
        "2",
        "@",
        "содержит",
        "стоп-слова",
        "и",
        "пунктуацию",
        "какие",
        "как",
        "!",
    ]
    preprocessor.filter_stopwords()
    assert preprocessor.tokens == [
        "это",
        "простой",
        "текст",
        ",",
        "!",
        "@",
        "содержит",
        "стоп-слова",
        "пунктуацию",
        "какие",
        "!",
    ]
    preprocessor.filter_punctuation()
    assert preprocessor.tokens == [
        "это",
        "простой",
        "текст",
        "",
        "",
        "",
        "содержит",
        "стопслова",
        "пунктуацию",
        "какие",
        "",
    ]
    preprocessor.stem_words()
    assert preprocessor.tokens == ["эт", "прост", "текст", "содерж", "стопслов", "пунктуац", "как"]
    tokens = preprocessor.preprocess()
    assert tokens == ["эт", "прост", "текст", "содерж", "стопслов", "пунктуац", "как"]
    query_string = preprocessor.get_query_string()
    assert query_string == "эт & прост & текст & содерж & стопслов & пунктуац & как"


@pytest.mark.django_db
def test_find_closest_request_returns_correct_request(request1, request2):
    """Test that the function returns the correct Request."""
    # request1 fixture contains the request "Test request"
    # Test should pass for all of the following strings:
    assert find_closest_request("Test request").request == request1.request
    assert find_closest_request("This is a test request").request == request1.request


@pytest.mark.django_db
def test_find_closest_request_returns_none_when_no_match(request1, request2):
    """Test that the function returns None when no matching Request is found."""
    assert find_closest_request("No match for this request") is None


@pytest.mark.django_db
def test_find_closest_request_with_empty_string(request1):
    """Test that the function returns None when an empty string is passed."""
    assert find_closest_request("") is None
