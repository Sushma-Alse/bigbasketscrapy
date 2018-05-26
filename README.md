This program is to extract prices of different items only for the site Big Basket. Currently tested only for Fruits and Vegetables category.

Steps to be followed to run this program are as below:
1. Get Splash up by running the following commands:
	a. sudo docker pull scrapinghub/splash (to be run only once)
	b. sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash 
Note: Install docker before running the above commands
For more details, follow the link below:
https://github.com/scrapinghub/splash/blob/master/docs/install.rst
This is required to get the dynamic Javascript code.

2. Update the urls to be tested in the file urls.csv in the main project file.

3. Run the program by giving the command: scrapy crawl bigbasket 

