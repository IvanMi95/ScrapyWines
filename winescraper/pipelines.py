# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from typing import Any, Dict
from itemadapter import ItemAdapter

from models.award import Award
from models.rating import Rating
from models.wine import Wine
from models.wine_info import WineInfo
from project.database import get_session
from util.print_util import custom_print, print_exception
from winescraper.util.pipe_util import clean_string, get_wine_type
from winescraper.util.tannico_util import convert_alcohol_percentage_to_float, convert_discount_percentage_tannico, convert_price_to_float_tannico, parse_availability
PRICES = ["sale_price", "original_price", "lowest_price"]


class TannicoPipeline:
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
                raw_type=adapter["wine_type"],
                url=adapter["url"]
            )
        return item


class WinescraperDataBasePipeline:
    def process_item(self, item: Dict[str, Any], spider):
        adapter = ItemAdapter(item)
        # TODO if price  noneskip price saving
        with get_session() as session:
            try:
                wine = session.query(Wine).filter(Wine.url == adapter["url"]).first()
                if not wine:
                    wine = Wine(
                        website=adapter["website"],
                        url=adapter["url"],
                        vivino_url=adapter["vivino_url"],
                        name=adapter["name"],
                        grape_variety=adapter["grape_variety"],
                        appellation=adapter["appellation"],
                        alcohol_content=adapter["alcohol_content"],
                        serving_temperature=adapter["serving_temperature"],
                        wine_type=adapter["wine_type"]
                    )
                    for award_data in adapter.get("awards", []):
                        award = Award(critic=award_data["critic"], score=award_data["score"])
                        wine.awards.append(award)

                    session.add(wine)
                    session.flush()

                    wine_info = WineInfo(
                        wine_id=wine.id,
                        source=adapter["website"],
                        sale_price=adapter["sale_price"],
                        original_price=adapter["original_price"],
                        lowest_price=adapter["lowest_price"],
                        discount_percentage=adapter["discount_percentage"],
                        availability=adapter["availability"],
                    )
                    session.add(wine_info)
                    rating = Rating(
                        wine_id=wine.id,
                        source=adapter["rating_source"],
                        score=adapter["vivino_rating"],
                        reviews=adapter["vivino_reviews"]
                    )
                    session.add(rating)
                else:
                    if wine.alcohol_content is None:
                        wine.alcohol_content = adapter["alcohol_content"]
                    if wine.appellation is None:
                        wine.appellation = adapter["appellation"]
                    if wine.grape_variety is None:
                        wine.grape_variety = adapter["grape_variety"]
                    if wine.serving_temperature is None:
                        wine.serving_temperature = adapter["serving_temperature"]

                    for award_data in adapter.get("awards", []):
                        award = session.query(Award).filter(
                            Award.critic == award_data["critic"],
                            Award.wine_id == wine.id
                        ).order_by(Award.id.desc()).first()
                        if not award:
                            award = Award(
                                wine_id=wine.id,
                                critic=award_data["critic"],
                                score=award_data["score"]
                            )
                            session.add(award)
                        elif award_data["score"] != award.score:
                            award = Award(
                                wine_id=wine.id,
                                critic=award_data["critic"],
                                score=award_data["score"]
                            )
                            session.add(award)
                    wine_info = session.query(WineInfo).filter(
                        WineInfo.source == adapter["website"],
                        WineInfo.wine_id == wine.id
                    ).order_by(WineInfo.id.desc()).first()
                    if not wine_info:
                        wine_info = WineInfo(
                            wine_id=wine.id,
                            source=adapter["website"],
                            sale_price=adapter["sale_price"],
                            original_price=adapter["original_price"],
                            lowest_price=adapter["lowest_price"],
                            discount_percentage=adapter["discount_percentage"],
                            availability=adapter["availability"],
                        )
                        session.add(wine_info)
                    elif (
                        wine_info.availability != adapter["availability"] or
                        wine_info.sale_price != adapter["sale_price"] or
                        wine_info.discount_percentage != adapter["discount_percentage"]
                    ):
                        wine_info = WineInfo(
                            wine_id=wine.id,
                            source=adapter["website"],
                            sale_price=adapter["sale_price"],
                            original_price=adapter["original_price"],
                            lowest_price=adapter["lowest_price"],
                            discount_percentage=adapter["discount_percentage"],
                            availability=adapter["availability"],
                        )
                        session.add(wine_info)
                    rating = session.query(Rating).filter(
                        Rating.source == adapter["rating_source"],
                        Rating.wine_id == wine.id
                    ).order_by(Rating.id.desc()).first()
                    if not rating:
                        rating = Rating(
                            wine_id=wine.id,
                            source=adapter["rating_source"],
                            score=adapter["vivino_rating"],
                            reviews=adapter["vivino_reviews"]
                        )
                        session.add(rating)
                    elif (
                        rating.score != adapter["score"] or
                        rating.reviews != adapter["reviews"]
                    ):
                        rating = Rating(
                            wine_id=wine.id,
                            source=adapter["rating_source"],
                            score=adapter["vivino_rating"],
                            reviews=adapter["vivino_reviews"]
                        )
                        session.add(rating)

                session.commit()
            except Exception as exc:
                session.rollback()
                print_exception(exception=exc)
        return item
