#This program has been created to extract the prices from Big Basket
#It currently can extract the prices only from the category list of products, eg. Friuts and Vegetables
#Urls of the pages has to be proived in the excel-urls.csv present in the main project folder
#DO NOT CHANGE THE NAME/EXTENSION OF urls.csv
#This program generates an output file-prices-(date-time).csv, which extracts the product item, mrp and final price

import scrapy
import csv
from itertools import zip_longest
import datetime
import re
import json

class ProductPriceSpider(scrapy.Spider):
	name = "bigbasket"

	def start_requests(self):
		#List of all urls to be searched. Commenting below code for testing
		urls = []

		#reading input csv file
		fileName = "urls.csv"
		with open(fileName, 'r') as f:
			for line in f.readlines():
				urls.append(line)

		self.log(urls)		

		#start extracting for all urls
		for url in urls:
			self.log(url)
			#For individual products call the link without splash as it has no dynamic code
			if "bigbasket.com/pd" in url:
				yield scrapy.Request(url=url, callback=self.parse_link)
			else:	
				yield scrapy.Request(url=url, callback=self.parse_link, meta={
					'splash': {
						'endpoint': 'render.html',
						'args': {'wait': 15.0}
						}	
               		})


	#Function for initially written for parsing url and extended pages
	#Currently not used
	def parse(self, response):
		#Later if Splash has to be replaced by scrapy.Webdriver
		#phantom_url = response.url.replace("http", "js-http")
		#yield scrapy.WebdriverRequest(url = response.url, callback = self.parseCompleteHtml)
		#le = LinkExtractor()
		#pattern = re.compile(r'^https://www.bigbasket.com/cl/fruits-vegetables/\?nc=nb/*')
		#for link in le.extract_links(response):
		
		#num_pages = 6
		#sid = response.xpath('//*[@id="filterbar"]/div[2]/div/div/div/div/div/a').re(r'sid=(\w+)')[0]

		for i in range(1,7):
			url = 'https://www.bigbasket.com/cl/fruits-vegetables/?nc=nb#!'
			#url = url + urllib.parse.urlencode({'sid': sid, 'page': str(i)})
			#url = url + urllib.parse.urlencode({'page': str(i)})
			yield scrapy.Request(url=url, callback=self.parse_link, meta={
				'splash': {
					'endpoint': 'render.html',
					'args': {'wait': 15.5}
					}
				})	

	#Parser specific for bigbasket htmls
	#Parser extracts item product name, quantity, MRP and final price
	def parse_link(self, response):			
		self.log(response.url)
		
		#For list of subcategories of items
		items = response.css("div.tab-content div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope").extract()
		
		#For individual product
		item = response.css("div.uiv2-product-detail-content.wid-250").extract_first()
		
		if items:
			self.log("Inside items")
			#Product title rows
			product_titles = []
			product_titles = response.css("div.tab-content div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope div.col-sm-12.col-xs-7.prod-name a::attr(uib-tooltip)").extract()
			self.log(product_titles)

			#Product measurement rows
			product_measures = []
			measure_rows = response.css("div.tab-content div.items div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope div.col-sm-12.col-xs-7.qnty-selection div.btn-group.btn-input.clearfix.ng-scope span.ng-scope span.ng-binding").extract()
			#self.log(measure_rows)
			extra = "vm.selectedProduct.w"
			measure_rows = [e for e in measure_rows if extra in e]
			self.log(measure_rows)
			#Extract only the required value from the string	
			for row in measure_rows:
				product_measures.append(row.split(">")[1].split("<")[0])
			self.log(product_measures)
			
			#Product MRP rows
			product_mrps = []
			mrp_rows = response.css("div.tab-content div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope div.col-sm-12.col-xs-12.add-bskt div.elements div.po-markup h4 span.mp-price span.ng-binding").extract()
			self.log(mrp_rows)
			#Extract only the MRP from the string	
			for row in mrp_rows:
				product_mrps.append(row.split(">")[1].split("<")[0])
			self.log(product_mrps)

			#Product final prize rows
			product_prices = []
			offer_rows = response.css("div.tab-content div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope div.col-sm-12.col-xs-12.add-bskt div.elements div.po-markup h4 span.discnt-price span.ng-binding").extract()
			self.log(offer_rows)
			#Extract the final price from the string	
			for row in offer_rows:
				product_prices.append(row.split(">")[1].split("<")[0])
			self.log(product_prices)

		elif item is not None:
			self.log("Inside item")
			#Product title rows
			product_titles = []
			title = response.css("div.uiv2-product-detail-content.wid-250 div.uiv2-product-name h1").extract_first().split("Fresho ")[1].split(" \n")[0]
			product_titles.append(title)
			self.log(product_titles)

			#Product measurement rows
			product_measures = []
			measure = response.css("div.uiv2-product-detail-content.wid-250 div.uiv2-product-size div.uiv2-size-variants label").extract_first().split("<label>")[1].split("\n")[0]
			product_measures.append(measure)
			self.log(product_measures)

			#Product MRP rows
			product_mrps = []
			mrp = response.css("div.uiv2-product-detail-content.wid-250 div.uiv2-product-value div.uiv2-savings div.uiv2-mrp").extract_first().split("Rs ")[1].split("<")[0]
			product_mrps.append(mrp)
			self.log(product_mrps)

			#Product final prize rows
			product_prices = []
			price = response.css("div.uiv2-product-detail-content.wid-250 div.uiv2-product-value div.uiv2-price").extract_first().split("Rs. ")[1].split("<")[0]
			product_prices.append(price)
			self.log(product_prices)


		#Write the extracted data into an output csv file
		fileName = 'prices-%s.csv' %datetime.datetime.now().strftime("%m-%d-%H-%M")
		with open(fileName, 'a') as f:
			writer = csv.writer(f)
			writer.writerows(zip(product_titles, product_measures, product_mrps, product_prices))
