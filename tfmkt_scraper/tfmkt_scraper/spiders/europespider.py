import scrapy


class EuropespiderSpider(scrapy.Spider):
    name = "europespider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/wettbewerbe/europa"]

    def parse(self, response):
        table_rows = response.css('table.items tbody tr.odd, table.items tbody tr.even')
        for row in table_rows:
            yield{
                'league_url': row.css('a').attrib['href']
            }
        
        next_page = response.css('li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.transfermarkt.com' + next_page
            yield response.follow(next_page_url, callback= self.parse)