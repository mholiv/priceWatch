from bs4 import BeautifulSoup
import urllib.request
from sql import alcsession, Price



url = 'http://www.bulkammo.com/rifle/bulk-7.62x39mm-ammo'
#url = 'http://www.bulkammo.com/rifle/bulk-5.45x39mm-ammo'
#url = 'http://www.bulkammo.com/rifle/bulk-.223-ammo'
#url = 'http://www.bulkammo.com/handgun/bulk-9mm-ammo'
#First we grab the messy raw html
messyHtml = urllib.request.urlopen(url)
soup = BeautifulSoup(messyHtml, 'html.parser')

#Next we isolate the product grid, then the first (cheapest) ammo.
allItemList = soup.find("ul", {"class": "products-grid"})
cheapestRound = allItemList.find("li", {"class": "first"})

#We get the name of the ammo. It is stored in a href in a h2 header.
nameOfAmmo = cheapestRound.h2.a.string

#Next we get the quantity.
quantityOfAmmo= cheapestRound.find("span", {"class": "stock-qty"}).string.strip()


#We need to worry about 'special' prices. Check and see if it exists
specialPrice = cheapestRound.find("p", {"class": "special-price"})

#We get the count of rounds. THis assumes the count is always the first word.
roundCount = int(nameOfAmmo.split(' ')[0])

#If it does not exist use the use the normal price, else use special price
if specialPrice == None:
    costOfAmmo = float(cheapestRound.find("span", {"class": "price"}).string.strip()[1:])
else:
    costOfAmmo = float(specialPrice.find("span", {"class": "price"}).string.strip()[1:])
costPerRound= format(costOfAmmo/roundCount, '.3f')



print('\n',nameOfAmmo,'\n',costOfAmmo,'\n',quantityOfAmmo,'\n',roundCount,'\n',costPerRound)
