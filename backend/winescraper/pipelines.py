# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any, Dict
from itemadapter import ItemAdapter

from winescraper.util.pipe_util import clean_string, get_wine_type
from winescraper.util.tannico_util import convert_alcohol_percentage_to_float, convert_discount_percentage_tannico, convert_price_to_float_tannico, parse_availability
PRICES = ["sale_price", "original_price", "lowest_price"]


class WinescraperPipeline:
    def process_item(self, item: Dict[str, Any], spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'awards':
                adapter[field_name] = clean_string(value=adapter.get(field_name))

        for price in PRICES:
            if price in adapter:
                adapter[price] = convert_price_to_float_tannico(price_string=adapter[price])

        if "discount_percentage" in adapter:
            adapter["discount_percentage"] = convert_discount_percentage_tannico(
                original_price=adapter["original_price"],
                sale_price=adapter["sale_price"]
            )
        if "alcohol_content" in adapter:
            adapter["alcohol_content"] = convert_alcohol_percentage_to_float(
                percentage_string=adapter["alcohol_content"]
            )
        if "availability" in adapter:
            adapter["availability"] = parse_availability(
                availability=adapter["availability"]
            )
        if "wine_type" in adapter:
            adapter["wine_type"] = get_wine_type(
                raw_type=adapter["wine_type"]
            )
        return item
