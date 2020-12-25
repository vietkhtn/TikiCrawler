import scrapy
import re
from ..items import TikiProductInfo, TikiUserRating


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
        product_name = str(temp_productname.group().replace('\\u', R'\u')) #ten san pham (dang \u)

        product_price = re.search('(?<="price":).*?(?=,)', response.text)

        temp_productdescription = re.search('(?<="short_description":").*?(?=",)', response.text)
        product_description = str(temp_productdescription.group().replace('\\u', R'\u'))

        temp_productcategory = re.search('(?<="productset_group_name":").*?(?=",)', response.text)
        product_category = str(temp_productcategory.group().replace('\\u', R'\u'))
        product_category = str(temp_productcategory.group().replace('\/', ' - '))

        item['productID'] = product_id.group()
        item['productSKU'] = product_sku.group()
        item['productName'] = product_name
        item['productPrice'] = product_price.group()
        item['productDescription'] = product_description
        item['productCategory'] = product_category
        yield item

class UserRating(scrapy.Spider):
    name = "TikiUserRating"
    start_urls = ["https://tiki.vn/dien-gia-dung/c1882?src=c.1882.hamburger_menu_fly_out_banner"]

    def parse(self, response):
        listProduct = response.css(".product-item")

        for product in listProduct:
            # Lấy productID từ đường Link SP
            productLink = product.css("a::attr(href)").extract()
            temp = re.search('\d{6,8}', str(productLink))
            productID = temp.group()

            # Gọi tới API chứa thông tin sp lấy 50 comment
            url = f'https://tiki.vn/api/v2/reviews?product_id={productID}&sort=score|desc,id|desc,stars|all&page=1&limit=100'
            yield response.follow(url=url, callback=self.parseUserRating)

    def parseUserRating(self, response):
        userRating = TikiUserRating()
        userRateList = re.findall('(?<="full_name":").*?(?=",)', response.text)
        productRate = re.search('(?<="product_id":).*?(?=},)', response.text)
        timeRateList = re.findall('(?<="created_at":).*?(?=,)', response.text)
        startRateList = re.findall('(?<="rating":).*?(?=,)', response.text)
        commentRateList = re.findall('(?<="content":").*?(?=",")', response.text)
        for i in range(0, len(userRateList)):
            userRate = userRateList[i]
            timeRate = timeRateList[i]
            starRate = startRateList[i]
            commentRate = commentRateList[i]
            print(len(commentRate))
            if len(commentRate) > 0:
                if commentRate != '","status":"approved':
                    userRating['stt'] = i
                    userRating['userRate'] = userRate
                    userRating['productRate'] = productRate.group()
                    userRating['timeRate'] = timeRate
                    userRating['starRate'] = starRate
                    userRating['commentRate'] = commentRate
                    yield userRating


