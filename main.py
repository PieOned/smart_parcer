from scrapy.crawler import CrawlerProcess
from parse.spiders.b24 import B24Spider
from scrapy.utils.project import get_project_settings
import parse_settings

if __name__ == '__main__':
    settings = get_project_settings()
    settings.set('FEEDS', {
        f"{parse_settings.OUTPUT_FILE_NAME}.{parse_settings.OUTPUT_FILE_FORMAT}": {"format": parse_settings.OUTPUT_FILE_FORMAT}
    })

    process = CrawlerProcess(settings)
    process.crawl(B24Spider)
    process.start()
    
