from extratools_text import text_to_sentences


def test_text_to_sentences() -> None:
    assert text_to_sentences("") == []

    assert text_to_sentences("Hello there!") == [
        "Hello there!",
    ]

    assert text_to_sentences("Hello there! I am Bob.") == [
        "Hello there!",
        "I am Bob.",
    ]
