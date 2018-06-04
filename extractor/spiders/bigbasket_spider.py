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
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductPriceSpider(scrapy.Spider):
	name = "bigbasket"

	def __init__(self):
		self.driver = webdriver.Chrome('/usr/bin/chromedriver')
					 
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
			yield scrapy.Request(url=url, callback=self.parse_link)

	#Parser specific for bigbasket htmls
	#Parser extracts item product name, quantity, MRP and final price
	def parse_link(self, response):			
		self.log(response.url)
		self.driver.get(response.url)
		
		#For list of subcategories of items wait for 15secs or until element is loaded
		items = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tab-content div.item.prod-deck.row.ng-scope div.clearfix div.ng-scope"))
		)
		
		#For individual product
		item = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.uiv2-product-detail-content.wid-250"))
		)
	
		if items:
			self.log("Inside items")
			#Product title rows
			product_titles = []
			title_rows = self.driver.find_elements(By.XPATH, '//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div[1]/div[2]/div/div/product-template/div/div[4]/div/a')
			#Extract only the required value from the string
			for row in title_rows:
				product_titles.append(row.get_attribute('text'))
			self.log(product_titles)

			#Product measurement rows
			product_measures = []
			measure_rows = self.driver.find_elements(By.XPATH, '//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div[1]/div[2]/div/div/product-template/div/div[4]/div[2]/div//span[1]/span[@ng-bind="vm.selectedProduct.w"]')
			#Extract only the required value from the string
			for row in measure_rows:
				product_measures.append(row.text)
			self.log(product_measures)
			
			#Product MRP rows
			product_mrps = []
			mrp_rows = self.driver.find_elements(By.XPATH, '//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div[1]/div[2]/div/div/product-template/div/div[4]/div[3]/div/div/h4/span[1]/span')
			#Extract only the MRP from the string	
			for row in mrp_rows:
				product_mrps.append(row.text)
			self.log(product_mrps)

			#Product final prize rows
			product_prices = []
			offer_rows = self.driver.find_elements(By.XPATH, '//*[@id="dynamicDirective"]/product-deck/section/div[2]/div[4]/div[1]/div/div[1]/div[2]/div/div/product-template/div/div[4]/div[3]/div/div[1]/h4/span[2]/span')
			#Extract the final price from the string	
			for row in offer_rows:
				product_prices.append(row.text)
			self.log(product_prices)

		elif item is not None:
			self.log("Inside item")
			#Product title rows
			product_titles = []
			title = self.driver.find_element(By.XPATH, '//*[@id="slidingProduct*"]/div[2]/div[2]/h1').text
			product_titles.append(title)
			self.log(product_titles)

			#Product measurement rows
			product_measures = []
			#measure = self.driver.find_element(By.CSS_SELECTOR, "div.uiv2-product-detail-content.wid-250 div.uiv2-product-size div.uiv2-size-variants label").split("<label>")[1].split("\n")[0]
			#measure = sel.select("div.uiv2-product-detail-content.wid-250 div.uiv2-product-size div.uiv2-size-variants label")[0].split("<label>")[1].split("\n")[0]
			#product_measures.append(measure)
			#self.log(product_measures)

			#Product MRP rows
			product_mrps = []
			mrp = self.driver.find_element(By.XPATH, '//*[@id="slidingProduct*"]/div[2]/div[3]/div[3]/div/span[2]').text
			product_mrps.append(mrp)
			self.log(product_mrps)

			#Product final prize rows
			product_prices = []
			price = self.driver.find_element(By.XPATH, '//*[@id="slidingProduct"]/div[2]/div[3]/div[4]').text
			product_prices.append(price)
			self.log(product_prices)


		#Write the extracted data into an output csv file
		fileName = 'prices-%s.csv' %datetime.datetime.now().strftime("%m-%d-%H-%M")
		with open(fileName, 'a') as f:
			writer = csv.writer(f)
			writer.writerows(zip(product_titles, product_measures, product_mrps, product_prices))

	def tearDown(self):		
		self.driver.close()	
