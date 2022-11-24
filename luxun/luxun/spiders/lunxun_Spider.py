import scrapy
from luxun.items import Luxun_Book_Item, Luxun_Diary_Item

initial_url = "http://www.luxunmuseum.com.cn/cx/"
title_c2e = {"序号": 'index', "集名": 'book_name', "篇名": 'title', "署名": 'author', "体裁": 'category', "发表刊物": 'publication', "年/月/日": 'date', "内容": 'text', "月份": 'date'}

class luxunSpider(scrapy.Spider):
	#title_c2e = {"序号": 'index', "集名": 'book_name', "篇名": 'title', "署名": 'author', "体裁": 'category', "发表刊物": 'publication', "年/月/日": 'date', "内容": 'text', "月份": 'date'}
	name = "luxun"
	allowed_domians = ["http://www.luxunmuseum.com.cn"]
	start_urls = ["http://www.luxunmuseum.com.cn/cx/works.php"]

	def parse(self, response):
		for section in response.xpath('//div[@id = "con_one_1"]//a'):
			href = section.xpath('./@href').extract_first()
			title = section.xpath('./text()').extract_first()
			url = response.urljoin(href)#urljoin后面一个斜杠的内容不要，所以不用去掉最后一个斜杠的内容
			yield scrapy.Request(url, callback = self.parse_article_inf, meta = {'title': title})



	def parse_article_inf(self, response):
		section = response.xpath('//td[@id = "tabel_bg"]/..')
		if len(section) > 0:
			#前三个专题
			for subsection in section:
				item = Luxun_Book_Item()
				item['index'] = subsection.xpath('.//a[@href = "#"]/text()').extract_first()

				banner = subsection.xpath('./td/@data-tabel').extract()[1:-1]#包含一个''去掉
				data = subsection.xpath('.//td[@data-tabel]/div/text()').extract()
				banner_data = dict(zip(banner, data))
				#这样就不需要控制长度了
				for key, value in banner_data.items():
					item[title_c2e[key]] = value
				#获取正文内容	
				detail_page_url = subsection.xpath('.//a[@target = "_blank"]/@href').extract_first()
				next_url = response.urljoin(detail_page_url)
				yield scrapy.Request(next_url, callback = self.parse_text, meta = {'items': item})

			#有的板块有多个页面	
			next_page = response.xpath('//div[@class = "fanye"]//li[@class = "tt1"]/../@href').extract()
			current_page = response.xpath('//div[@class = "fanye"]//li[@class = "f_set"]/text()').extract_first()
			if len(next_page) > 1 or current_page == '1':
				#不可以这样判断，因为第一页也是如此
				#如果有前一页后一页或者是第一页的情况下（不能翻页的话也不能等于'1'
				# print("Next Page.")
				url = response.urljoin(next_page[-1])
				yield scrapy.Request(url, callback = self.parse_article_inf)
		else:
			#专题
			# print("在专题中")
			item = Luxun_Book_Item()
			item['title'] = response.meta['title']
			#print(item['title'])

			text_dic = response.xpath('//div[@class = "ctcontent"]')
			block = text_dic.xpath('./blockquote/text() | ./blockquote/h3/text()').extract()

			if len(block) > 0:
				item['text'] = block
			else:
				item['text'] = text_dic.xpath('./text()').extract()[-1]			

			yield item
			# yield scrapy.Request(response.url, callback = self.parse_text, meta = {'items': item})	
			

	def parse_text(self, response):
		item = response.meta['items']
		#text_dic = response.xpath('//div[@class = "ctcontent"]/text()').extract()
		#text = text_dic[-1]
		text_dic = response.xpath('//div[@class = "ctcontent"]')
		block = text_dic.xpath('./blockquote/text() | ./blockquote/h3/text()').extract()

		if len(block) > 0:
			item['text'] = block
		else:
			item['text'] = text_dic.xpath('./text()').extract()[-1]


		return item