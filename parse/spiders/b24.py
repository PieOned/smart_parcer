import scrapy
import parse_settings


class B24Spider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/']

    genre_dict = {
        "detectives": ["detektivy-1594", 361],
        "fiction": ["fantastika-1649", 217],
        "horrors": ["uzhasy-i-mistika-2054", 31],
        "fantasy": ["fentezi-1661", 227],
        "romance": ["lyubovnyy-roman-1622", 98],
        "action": ["boeviki-trillery-1715", 88]
    }

    genre_list = [genre.lower() for genre in parse_settings.GENRES]

    def start_requests(self):
        for genre in self.genre_list:
            link = self.genre_dict[genre][0]
            pages = self.genre_dict[genre][1]
            for page in range(1, 1 + pages):
                url = f'https://book24.ru/catalog/{link}/page-{page}/'
                yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.product-card__name::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'title': response.css('.product-detail-page__title::text').extract_first('').strip().split(':', 1)[1].strip(),
            'ISBN': response.css('.isbn-product::text').extract_first('').strip(),
            'author': response.css('.product-detail-page__title::text').extract_first('').strip().split(':', 1)[0].strip(),
            'description': ' '.join(response.css('.product-about__text p::text').extract()),
            'link': response.url
        }
        yield item
