from nltk import PunktSentenceTokenizer

__pst: PunktSentenceTokenizer | None = None


def text_to_sentences(text: str) -> list[str]:
    global __pst  # noqa: PLW0603

    if not __pst:
        __pst = PunktSentenceTokenizer()

    return __pst.tokenize(text)
