
def get_tannico_settings():
    return {
        "FEEDS": {
            "tannico_data.json": {"format": "json", "indent": 4, "overwrite": True}
        },
        "ITEM_PIPELINES": {
            "winescraper.pipelines.WinescraperPipeline": 300,
            "winescraper.pipelines.WinescraperDataBasePipeline": 400
        },
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "FEED_EXPORT_ENCODING": "utf-8",
        "ROBOTSTXT_OBEY": False,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 5,
        "AUTOTHROTTLE_MAX_DELAY": 60,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0

    }


def get_tannico_settings_without_vivino():
    return {
        "FEEDS": {
            "tannico_data_without_vivino.json": {"format": "json",  "indent": 4, "overwrite": True}
        },
        "ITEM_PIPELINES": {
            "winescraper.pipelines.WinescraperPipeline": 300
        },
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "FEED_EXPORT_ENCODING": "utf-8",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }
