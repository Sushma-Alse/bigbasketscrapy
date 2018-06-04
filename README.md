This program is to extract prices of different items only for the site Big Basket. Currently tested only for Fruits and Vegetables category.
There are two methods of running this program, either through splash or through selenim webdriver. These are required to load the dynamic Javascript. Both the methods are described below:

Splash:
Steps to be followed to run this program are as below:
1. Get Splash up by running the following commands:
	a. sudo docker pull scrapinghub/splash (to be run only once)
	b. sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash 
Note: Install docker before running the above commands
For more details, follow the link below:
https://github.com/scrapinghub/splash/blob/master/docs/install.rst
This is required to get the dynamic Javascript code.
2. Update the urls to be tested in the file urls.csv in the main project file.
3. Run the program by giving the command: scrapy crawl extractor 

Selenium webdriver:
1. pip install selenium
2. Install chromedriver and update the executable path in the the file extractor/extractor/spider/bigbasket_spider.py, in __init__(self) function. Currently provided with the path as below:
def __init__(self):
        self.driver = webdriver.Chrome('/usr/bin/chromedriver')
3. Update the urls to be tested in the file urls.csv in the main project file.
4. Run the program with command: scrapy crawl bigbasket

NOTE: Individual item url is currently not working, try it only for subcategories or urls
