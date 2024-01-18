CHOSUNG_START_LETTER = 4352
JAMO_START_LETTER = 44032
JAMO_END_LETTER = 55203
JAMO_CYCLE = 588


def is_hangul(ch) -> bool:
    return JAMO_START_LETTER <= ord(ch) <= JAMO_END_LETTER


def convert_to_initial_letters(hangul_text):
    result = ""
    for ch in hangul_text:
        if is_hangul(ch):
            result += chr(
                (ord(ch) - JAMO_START_LETTER) // JAMO_CYCLE + CHOSUNG_START_LETTER
            )
        else:
            result += ch

    return result
