def dividi_blocchi(testo: str, max_caratteri: int = 10000) -> list:
    """
    Divide il testo in blocchi da massimo `max_caratteri` caratteri.

    Utile per evitare problemi di lunghezza input nei modelli GPT.
    """
    return [testo[i:i + max_caratteri] for i in range(0, len(testo), max_caratteri)]
