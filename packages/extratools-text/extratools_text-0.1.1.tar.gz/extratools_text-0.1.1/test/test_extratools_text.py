from extratools_text import extract_noun_phrases, text_to_sentences


def test_text_to_sentences() -> None:
    assert text_to_sentences("") == []

    assert text_to_sentences("Hello there!") == [
        "Hello there!",
    ]

    assert text_to_sentences("Hello there! I am Bob.") == [
        "Hello there!",
        "I am Bob.",
    ]


def test_extract_noun_phrases() -> None:
    assert extract_noun_phrases("") == []

    assert extract_noun_phrases(
        "The quick brown fox jumps over the lazy dog and runs away.",
        normalize=False,
    ) == [
        "The quick brown fox",
        "the lazy dog",
    ]

    assert extract_noun_phrases(
        "The quick brown fox jumps over the lazy dog and runs away.",
    ) == [
        "quick brown fox",
        "lazy dog",
    ]
