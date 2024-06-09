# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any, Dict
from itemadapter import ItemAdapter

from project.database import get_session
from project.wines.models import Award, Wine
from util.print_util import print_exception
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
            else:
                adapter[field_name] = [
                    {
                        "critic": clean_string(value=award_data["critic"]),
                        "score": clean_string(value=award_data["score"])

                    }
                    for award_data in adapter.get("awards", [])
                ]

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


class WinescraperDataBasePipeline:
    def process_item(self, item: Dict[str, Any], spider):
        adapter = ItemAdapter(item)
        with get_session() as session:
            try:
                wine = session.query(Wine).filter(Wine.url == adapter["url"]).first()
                if not wine:
                    wine = Wine(
                        website=adapter["website"],
                        url=adapter["url"],
                        name=adapter["name"],
                        sale_price=adapter["sale_price"],
                        original_price=adapter["original_price"],
                        lowest_price=adapter["lowest_price"],
                        discount_percentage=adapter["discount_percentage"],
                        availability=adapter["availability"],
                        grape_variety=adapter["grape_variety"],
                        appellation=adapter["appellation"],
                        alcohol_content=adapter["alcohol_content"],
                        serving_temperature=adapter["serving_temperature"],
                        wine_type=adapter["wine_type"],
                        vivino_rating=adapter["vivino_rating"],
                        vivino_reviews=adapter["vivino_reviews"],
                        vivino_url=adapter["vivino_url"]
                    )
                    for award_data in adapter.get("awards", []):
                        award = Award(critic=award_data["critic"], score=award_data["score"])
                        wine.awards.append(award)
                    session.add(wine)
                else:
                    wine.sale_price = adapter["sale_price"]
                    wine.original_price = adapter["original_price"]
                    wine.lowest_price = adapter["lowest_price"]
                    wine.discount_percentage = adapter["discount_percentage"]
                    wine.availability = adapter["availability"]
                    wine.appellation = adapter["appellation"]
                    wine.grape_variety = adapter["grape_variety"]
                    wine.alcohol_content = adapter["alcohol_content"]
                    wine.serving_temperature = adapter["serving_temperature"]
                    wine.vivino_rating = adapter["vivino_rating"]
                    wine.vivino_reviews = adapter["vivino_reviews"]
                    for award_data in adapter.get("awards", []):
                        award = session.query(Award).filter(
                            Award.critic == award_data["critic"],
                            Award.wine_id == wine.id
                        ).first()
                        if not award:
                            award = Award(
                                wine_id=wine.id,
                                critic=award_data["critic"],
                                score=award_data["score"]
                            )
                            session.add(award)
                        else:
                            award.score = award_data["score"]
                session.commit()
            except Exception as exc:
                session.rollback()
                print_exception(exception=exc)
