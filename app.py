# © ebay_scraper- Made by Yuval Simon. For bogan.cool

import requests, math
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
import csv


url = input("Please enter ebay's url: ")
budget = int(input("Please enter your product's budget in USD: "))
currency = input('Please enter your currency in caps: ')
c = CurrencyConverter()


req = requests.get(f'{url}&_ipg=200')
soup = BeautifulSoup(req.text, 'lxml')
div = soup.find('div', {'id': "srp-river-results"})
ul = div.find('ul', {'class': "srp-results srp-list clearfix"})


for i in range(200):
    table = ul.find_all('li', {'data-view': f"mi:1686|iid:{i}"})

    for t in table:
        name = table[0].find('a', {'class': "s-item__link"})
        price = table[0].find('span', {'class': 's-item__price'})
        prices = price.text

        remove = [f"{currency}", ","]
        for r in remove:
            prices = prices.replace(r, "")

        convert = c.convert(prices, f'{currency}', 'USD')
        convert = math.trunc(convert)

        if convert < budget:
            print(f'{name.text} ---> Price:{convert} USD')
        
        else:
            pass