import re
from typing import Any, Optional
WHITE = ["bianco", "white", "vini bianchi"]
RED = ["rosso", "red", "vini rossi"]
CHAMPAGNE = ["champagne"]
SPARKLING = ["sparkling wine", "spumante", "spumanti"]
DESSERT = ["dolce", "dessert"]
ROSE = ["rosé", "rose", "vini rosati"]
FORTIFIED = ["vini liquorosi", "fortified wine"]
INVALID = ["gin", "liquori e altri distillati"]


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
        '»': '',
        '\u00a0': '',
        "\n": ""
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


def get_wine_type(raw_type: str, url: str = "") -> str:
    try:
        wine_type = raw_type.lower()
        if wine_type in WHITE:
            return "white"
        if wine_type in RED:
            return "red"
        if wine_type in CHAMPAGNE:
            return "champagne"
        if wine_type in SPARKLING:
            return "sparkling"
        if wine_type in DESSERT:
            return "dessert"
        if wine_type in ROSE:
            return "rose"
        if wine_type in FORTIFIED:
            return "fortified"
        if wine_type in INVALID:
            return None
        # TODO add in saving pipeline check if wine type is none
        with open("error_log.txt", 'a') as file:
            file.write(f"wine type -> {wine_type} \n  {url} \n")
        return "Error parsing type"
    except KeyError:
        return "Error parsing type"


def append_to_file(file_path, text):
    try:
        with open(file_path, 'a') as file:
            file.write(text + '\n')
        print(f"Successfully appended to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
