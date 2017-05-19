from selenium import webdriver

class AmazonProduct:
	link = ""
	name = ""
	price = 0.0
	brand = ""
	asin = ""
	scrapeLevel = 0
	def dataOne(self, link, name, brand, price, asin):
		self.link = link
		self.name = name
		self.brand = brand
		self.price = price
		self.asin = asin # ARE YOU ASIN?
		self.scrapeLevel = 1
	def toDict(self):
		return {"link": self.link,
				"name": self.name,
				"price": self.price,
				"brand": self.brand,
				"asin": self.asin}

class AmazonScraper:
	PRODUCTS = []
	def __init__(self):
		self.wh = webdriver.Chrome()
	def navToCategory(self, category, subcategory):
		self.wh.get("https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn")
		depts = self.wh.find_elements_by_class_name("fsdDeptLink")
		for dept in depts:
			if dept.text.lower() == category.lower():
				dept.click()
				break
		subcats = self.wh.find_elements_by_class_name("list-item__category-link")
		for sc in subcats:
			if sc.text.lower() == subcategory.lower():
				hr = sc.get_attribute("href")
				self.wh.get(hr)
				break
	def scrapeProducts(self):
		prods = self.wh.find_elements_by_class_name("s-result-item")
		for prod in prods:
			asin = prod.get_attribute("data-asin")
			name = prod.find_elements_by_class_name("s-access-title")[0].get_attribute("data-attribute")
			try:
				price = float(prod.find_elements_by_class_name("s-access-title")[0].text.replace("$"))
			except:
				price_whole = int(prod.find_elements_by_class_name("sx-price-whole")[0].text)
				price_half = int(prod.find_elements_by_class_name("sx-price-fractional")[0].text)
				price = price_whole + (price_half/100.0)
			brand = prod.find_elements_by_class_name("a-color-secondary")[1].text
			if brand == "by":
				brand = prod.find_elements_by_class_name("a-color-secondary")[2].text
			link = prod.find_elements_by_class_name("s-color-twister-title-link")[0].get_attribute("href")
			prodbaton = AmazonProduct()
			prodbaton.dataOne(link, name, brand, price, asin)
			self.PRODUCTS += [prodbaton]
			
################################
## simple run-cycle for debug ##
def doscrape():				  ##
	import os				  ##
	os.environ["PATH"] = os.environ["PATH"]+";."
	s=AmazonScraper()		  ##
	s.navToCategory("Headphones", "earbud headphones")
	s.scrapeProducts()		  ##
	return s				  ##
################################