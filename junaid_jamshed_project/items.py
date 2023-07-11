import scrapy


class ClothingItem(scrapy.Item):
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_images = scrapy.Field()
    product_info = scrapy.Field()
    product_code = scrapy.Field()
    values = scrapy.Field()
    
