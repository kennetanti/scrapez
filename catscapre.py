import amascrape
import json

print "Init main Amazon Scraper..."
ama = amascrape.AmazonScraper()
print "Scraping category list..."
cats = ama.getCategories()
print "Got "+str(len(cats))+" categories."
masterlist = {}
for cat in cats[cats.index("TV & Video"):]: #skip to relevant shit
	try:
		print "Getting subcategories for "+str(cats.index(cat))+"/"+str(len(cats))+" ["+cat+"]..."
		subcats = ama.getSubCategories(cat)
		print "Found "+str(len(subcats))+" subcategories"
		masterlist[cat] = subcats
	except:
		print "some error..fml"
print "Scraped all. dumping to cats.json"
with open("cats.json", "w") as fd:
	fd.write(json.dumps(masterlist))
print "done."