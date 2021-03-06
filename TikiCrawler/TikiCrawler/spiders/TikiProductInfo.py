import scrapy
import re
from ..items import TikiProductInfo


class ProductItem(scrapy.Spider):
    name = "TikiProductInfo"
    start_urls = ["https://tiki.vn/dien-gia-dung/c1882?src=c.1882.hamburger_menu_fly_out_banner"]

    def parse(self, response):
        listProduct = response.css(".product-item")

        for product in listProduct:
            # Lấy productID từ đường Link SP
            productLink = product.css("a::attr(href)").extract()
            temp = re.search('\d{6,8}', str(productLink))
            productID = temp.group()

            #Gọi tới API chứa thông tin sp
            url = f'https://tiki.vn/api/v2/products/{productID}?platform=web&spid=22486787&include=tag,images,gallery,promotions,badges,stock_item,variants,product_links,discount_tag,ranks,breadcrumbs,top_features,cta_desktop'
            yield response.follow(url=url, callback=self.parseProductInfo)

    def parseProductInfo(self, response):
        item = TikiProductInfo()
        product_id = re.search('(?<="id":).*?(?=,)', response.text) #id san pham
        product_sku = re.search('(?<="sku":").*?(?=",)', response.text) # SKU san pham

        temp_productname = re.search('(?<="name":").*?(?=",)', response.text) #Phan tich ra tên sp dạng \\u
        product_name = str(temp_productname.group().replace('\\/','/'))

        product_price = re.search('(?<="price":).*?(?=,)', response.text)

        temp_productdescription = re.search('(?<="short_description":").*?(?=",)', response.text)
        temp_productdescription = str(temp_productdescription.group().replace('"',"").lstrip('\n'))
        temp_productdescription = temp_productdescription.lstrip('\n')
        product_description = str(temp_productdescription.replace('"',"").replace('\\/','/'))

        temp_productcategory = re.search('(?<="productset_group_name":").*?(?=",)', response.text)
        product_category = str(temp_productcategory.group().replace('"',"").replace('\/', ' - '))

        item['productID'] = product_id.group()
        item['productSKU'] = product_sku.group()
        item['productName'] = product_name.encode().decode('unicode_escape')
        item['productPrice'] = product_price.group()
        item['productDescription'] = product_description.encode().decode('unicode_escape')
        item['productCategory'] = product_category.encode().decode('unicode_escape')
        yield item




