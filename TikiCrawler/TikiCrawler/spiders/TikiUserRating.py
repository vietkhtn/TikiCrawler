import scrapy
import re
from ..items import TikiUserRating

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