from bs4 import BeautifulSoup
import urllib.request
from sql import alcsession, Price
import datetime

def getBulkAmmoComData(site,path):
    #First we grab the messy raw html
    messyHtml = urllib.request.urlopen('http://%s%s'%(site,path))
    soup = BeautifulSoup(messyHtml, 'html.parser')

    #Next we isolate the product grid, then the first (cheapest) ammo.
    allItemList = soup.find("ul", {"class": "products-grid"})
    cheapestRound = allItemList.find("li", {"class": "first"})

    #We get the name of the ammo. It is stored in a href in a h2 header.
    nameOfAmmo = cheapestRound.h2.a.string

    #Next we get the quantity.
    quantityOfAmmo= int(cheapestRound.find("span", {"class": "stock-qty"}).string.strip())


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

    return {'nameOfAmmo':nameOfAmmo,
            'costOfAmmo':costOfAmmo,
            'quantityOfAmmo':quantityOfAmmo,
            'roundCount':roundCount,
            'costPerRound':costPerRound,
            'source':site,
            'date': datetime.datetime.now()
            }
