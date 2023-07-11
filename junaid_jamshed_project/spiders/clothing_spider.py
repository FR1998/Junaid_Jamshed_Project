from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from junaid_jamshed_project.items import ClothingItem


class ClothingSpider(CrawlSpider):
    name = "j_dot_spider"
    allowed_domains = ["junaidjamshed.com"]
    start_urls = ["https://www.junaidjamshed.com/"]
    country_code = "Pakistan" 
    
    rules = [
        Rule(
            LinkExtractor(
                allow="https://www.junaidjamshed.com/", 
                restrict_css="ul.columns-group li.megamenu.level1 a[href*='/mens']", 
                attrs="href"
            ), 
            follow=True
        ),
        Rule(
            LinkExtractor(
                restrict_css="a.product.photo.product-item-photo", 
                attrs="href"
            ), 
            callback="parse_clothing_product", 
            follow=True
        ),
        Rule(LinkExtractor(restrict_css="a.action.next", attrs="href"), follow=True),
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={"country_code":self.country_code})

    def extract_name(self, response):
        return response.css(".base::text").get()
    
    def extract_price(self, response):
        return response.css(".price::text").get()
    
    def extract_images(self, response):
        return response.css(".MagicToolboxSelectorsContainer div img::attr(src)").getall()
    
    def extract_additional_info(self, response):
        return response.css("#product-attribute-specs-table .data::text").getall()
    
    def extract_code(self, response):
        return response.css(".value::text").get()

    def parse_clothing_product(self, response):
        item = ClothingItem()
        
        item["product_name"] = self.extract_name(response)
        item["product_price"] = self.extract_price(response)
        item["product_images"] = self.extract_images(response)
        item["product_info"] = self.extract_additional_info(response)
        item["product_code"] = self.extract_code(response)
        
        yield item
    
