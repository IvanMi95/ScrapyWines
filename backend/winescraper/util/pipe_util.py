import re
from typing import Any, Optional
WHITE = ["bianco"]
RED = ["rosso"]


def remove_quotes(string: str) -> str:
    translation_table = str.maketrans({
        '“': '',
        '”': '',
        '"': '',
        '‘': '',
        '’': '',
        '„': '',
        '‟': '',
        '‹': '',
        '›': '',
        '«': '',
        '»': ''
    })
    return string.translate(translation_table)


def remove_encoded_characters(string: str) -> Optional[str]:
    pattern = r'[\x00-\x1F\x7F]'
    cleaned_string = re.sub(pattern, '', string).strip()
    return cleaned_string


def clean_string(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return value
    value = remove_quotes(string=value)
    value = remove_encoded_characters(string=value)
    return value


def get_wine_type(raw_type: str) -> str:
    try:
        wine_type = raw_type.lower()
        if wine_type in WHITE:
            return "white"
        if wine_type in RED:
            return "red"
    except KeyError:
        return "Error parsing type"
