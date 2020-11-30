import scrapy
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider


class Product(scrapy.Item):
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    product_category = scrapy.Field()
    price = scrapy.Field()
    sale_price = scrapy.Field()
    # price_before_sale = scrapy.Field()
    description = scrapy.Field()
    img_urls = scrapy.Field()


class NikeProductsSpider(SitemapSpider):
    name = 'NikeProducts'
    sitemap_urls = ['https://www.nike.com/sitemap-pdp-en-us.xml']
    def parse(self, response):
        item = Product()
        item['product_name'] = response.xpath("//div[@class='pr2-sm css-1ou6bb2']/h1/text()").get()
        item['product_category'] = response.xpath("//div[@class='pr2-sm css-1ou6bb2']/h2/text()").get()
        full_price = response.xpath("//div[@class='product-price css-11s12ax is--current-price']/text()").get()
        price_before_sale = response.xpath("//div[@class='product-price css-1h0t5hy']/text()").get()
        if full_price is not None:
            item['price'] = full_price
        elif price_before_sale is not None:
            item['price'] = price_before_sale
        item['sale_price'] = response.xpath("//div[@class='product-price is--current-price css-s56yt7']/text()").get()
        item['description'] = response.xpath("//div[@class='description-preview body-2 css-1pbvugb']/p/text()").get()
        image_1 = response.xpath("//div[@class='colorway-images ta-sm-c d-lg-t']//img/@src").getall()
        image_2 = response.xpath("//div[@class='css-du206p']//img/@src").getall()
        image_3 = response.xpath("//div[@class='css-1lvkqmp ']//img/@src").getall()
        image_4 = response.xpath("//div[@class='css - edayh7']//img/@src").getall()
        image_5 = response.xpath("//div[@class='css-1n3u4rt']//img/@src").getall()
        item['img_urls'] = image_1 + image_2 + image_3 + image_4 + image_5
        item['product_url'] = response.url
        return item

