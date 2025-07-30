from collections import Counter
from typing import Any

import spacy
from toolz.itertoolz import unique

__nlp = None


def __load_doc(text: str) -> Any:
    global __nlp  # noqa: PLW0603
    if not __nlp:
        __nlp = spacy.load("en_core_web_trf")

    return __nlp(text)


def text_to_sentences(text: str) -> list[str]:
    return [
        str(sentence)
        for sentence in __load_doc(text).sents
    ]


def extract_noun_phrases(
    text: str,
    *,
    # Including stop word removal
    normalize: bool = True,
) -> list[str]:
    nps: list[str] = [
        " ".join(
            str(token)
            for token in np
            if not token.is_stop and str(token).isalnum()
        ) if normalize else str(np)
        for np in (__load_doc(text).noun_chunks)
    ]

    return (
        list(unique(
            (np for np in nps if len(np) > 0),
            key=lambda np: np.lower(),
        )) if normalize
        else nps
    )


def extract_entities(
    text: str,
) -> Counter[tuple[str, str]]:
    return Counter(
        (str(entity.text), str(entity.label_))
        for entity in (__load_doc(text).ents)
    )
