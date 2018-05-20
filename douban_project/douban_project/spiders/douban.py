# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    '''豆瓣爬虫'''

    name = 'douban'
    allowed_domains = ['book.douban.com']
    # start_urls = ['http://book.douban.com/tag/']

    def start_requests(self):
        '''必须返回一个可迭代对象'''
        urls = [
            'https://book.douban.com/tag/?view=type'
        ]
        print('要开始爬取了')
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)



    def parse(self, response):
        '''解析首页内容'''
        # article = response.css('.article').extract() # extract用于解析对象吧，还有个extract_first方法

        ret = response.xpath("//div[@class='article']/div[2]/div")  # 得到的是个对象list
        base_url = 'https://book.douban.com'
        for each_category in ret:
            # category_name = each_category.xpath("./a")[0].get_attribute('name')    # 当前节点下边的a标签（失败，取不到值）
            category_name = each_category.xpath("./a/@name")[0].extract()  # 当前节点下边的a标签的name属性的值
            category_small_list = each_category.xpath(".//td/a")

            for small_category in category_small_list:

                url = small_category.xpath("./@href").extract_first()
                url = base_url + url
                small_category_name = small_category.xpath("./text()").extract_first()
                print(url,small_category_name)

        # 解析的返回值是Request，item对象(还有dict等，调度器会识别是什么对象)
