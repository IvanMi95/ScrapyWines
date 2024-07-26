import asyncio
from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess

from project.celery_utils import create_celery
from project.wines import wine_router
from winescraper.config.settings_config import get_tannico_settings, get_tannico_settings_without_vivino
from winescraper.spiders.tannicospider import TannicoSpider


def create_app() -> FastAPI:
    app = FastAPI()
    app.celery_app = create_celery()

    app.include_router(wine_router)

    # @app.get("/")
    # async def root():
    #     # Replace 'tannico_spider' with your spider name
    #     command = ["scrapy", "crawl", "tannicospider"]
    #     # Replace with the correct path to your project
    #     process = subprocess.Popen(command, cwd="/app")
    #     process.wait()  # Wait for the process to complete
    #     return {"message": "Crawling finished"}

    @app.get("/")
    async def root():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, run_crawler)
        return {"message": "Crawling finished"}

    def run_crawler():
        # process = CrawlerProcess(get_tannico_settings())
        process = CrawlerProcess(get_tannico_settings_without_vivino())
        process.crawl(TannicoSpider)
        # the script will block here until the crawling is finished
        # process.start(stop_after_crawl=True)
        process.start()  # This will block until the crawling is finished
        # process.stop()
    return app
