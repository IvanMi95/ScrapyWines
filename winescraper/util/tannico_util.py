from typing import Any, Optional


def convert_price_to_float_tannico(price_string: str) -> Optional[float]:
    if not isinstance(price_string, str):
        return price_string
    price_string = price_string.replace(",", ".").replace("€", "")
    return float(price_string)


# def convert_discount_percentage_tannico(discount_string: Any) -> Optional[float]:
#     if not isinstance(discount_string, str):
#         if isinstance(discount_string, float) or isinstance(discount_string, int):
#             return discount_string
#         return None

#     discount_string_list = discount_string.split(" ")

#     if not discount_string or discount_string == "Promozione" or len(discount_string_list) < 2:
#         if original_price == 0:
#             return
#         discount_percentage = ((original_price - sale_price) / original_price) * 100
#         return discount_percentage
#         return None
#     discount_string = discount_string_list[1].replace("%", "")
#     try:
#         discount = int(discount_string)
#     except ValueError:
#         return None

#     if discount > 0:
#         return discount/100

def convert_discount_percentage_tannico(original_price: float, sale_price: float) -> float:
    if original_price == 0:
        raise ValueError("Original price cannot be zero.")
    sale_percentage = ((original_price - sale_price) / original_price)
    return round(sale_percentage, 3)


def convert_alcohol_percentage_to_float(percentage_string: Any) -> Optional[float]:
    if not isinstance(percentage_string, str):
        if isinstance(percentage_string, float):
            return percentage_string
        return None
    percentage_string = percentage_string.replace("%", "")
    try:
        percentage = float(percentage_string)
    except ValueError:
        return None

    if percentage > 0:
        return percentage/100


def parse_availability(availability: Any) -> Optional[int]:
    if not isinstance(availability, str):
        return None
    if availability == "In pronta consegna":
        return 10000
    if availability == "In pronta consegna (solo un prodotto)":
        return 1
    availability_list = availability.split(" ")
    if len(availability_list) < 6:
        return None
    try:
        return int(availability_list[5])
    except ValueError:
        return None
