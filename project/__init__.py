import asyncio
import subprocess
from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess

from project.celery_utils import create_celery
from project.wines import wine_router
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
        process = CrawlerProcess(
            settings={
                "FEEDS": {
                    "winedata.json": {"format": "json"}
                },
                "ITEM_PIPELINES": {
                    "winescraper.pipelines.WinescraperPipeline": 300,
                },
                "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
                "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
                "FEED_EXPORT_ENCODING": "utf-8",
                "ROBOTSTXT_OBEY": False,

            }
        )
        process.crawl(TannicoSpider)
        # the script will block here until the crawling is finished
        # process.start(stop_after_crawl=True)
        process.start()  # This will block until the crawling is finished
        # process.stop()
    return app
