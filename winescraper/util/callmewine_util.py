import re
from typing import Any, Optional


def parse_availability_callmewine(availability: Any) -> Optional[int]:
    if availability is None:
        return 10000
    if not isinstance(availability, str):
        return None
    if availability == "Non disponibile":
        return None


def lowest_price_converter_cmw(price_string: Any) -> Optional[float]:
    if not isinstance(price_string, str):
        return None

    price_match = re.search(r"([\d,]+)€", price_string)
    if price_match:
        price_str = price_match.group(1)
        cleaned_price = price_str.replace(',', '.')
        return float(cleaned_price)
