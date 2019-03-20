from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess
from utilities import get_address

overview_page = 'https://web.archive.org/web/20150130033643/' \
                + 'http://www.americanwineryguide.com/regions/vineyards_list/california'


class WineSpider(Spider):
    name = 'wine_spider'

    def start_requests(self):
        yield Request(url=overview_page,
                      callback=self.parse_links)

    def parse_links(self, response):
        vineyards = response.css('ul#region_list li')
        for link in vineyards:
            date = response.url[28:36]
            date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            name = link.css(' ::text').extract()
            name = ''.join(name).strip()
            relative_link = response.css(' ::attr(href)').extract_first()
            absolute_link = response.urljoin(relative_link)

            overview_list.append([name, date, absolute_link])

            yield response.follow(url=absolute_link,
                                  callback=self.parse_vineyard)

        # Navigate to next date of page backup.
        yield Request(url=response.css('td.f ::attr(href)').extract_first(), callback=self.parse_links)

    def parse_vineyard(self, response):
        info = response.css('div#winery_detail_box1a *::text').extract()
        info = [line.strip() for line in info]
        # Remove empty lines
        info = [line for line in info if line]

        name = info[0]
        address = get_address(info)
        link = info[1]
        date = response.url[28:36]

        vineyards_list.append([name, date, address, link])

        # Scrape previous backup
        yield Request(url=response.css('td.b ::attr(href)').extract_first(), callback=self.parse_vineyard)
        # Scrapy next backup
        yield Request(url=response.css('td.f ::attr(href)').extract_first(), callback=self.parse_vineyard)


overview_list = []

vineyards_list = []

# Run the Spider
process = CrawlerProcess()
process.crawl(WineSpider)
process.start()
