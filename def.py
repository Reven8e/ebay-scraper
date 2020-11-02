# © ebay_scraper- Made by Yuval Simon. For bogan.cool

import requests, math
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter
import csv


url = input("Please enter ebay's url: ")
budget = int(input("Please enter your product's budget in USD: "))
currency = input('Please enter your currency in caps: ')
c = CurrencyConverter()

def finder(currency, budget, url):
    req = requests.get(f'{url}&_ipg=200')
    soup = BeautifulSoup(req.text, 'lxml')
    div = soup.find('div', {'id': "srp-river-results"})
    ul = div.find('ul', {'class': "srp-results srp-list clearfix"})

    for i in range(200):
        table = ul.find_all('li', {'data-view': f"mi:1686|iid:{i}"})

        for _ in table:
            name = table[0].find('a', {'class': "s-item__link"})
            link = table[0].find('a', {'class': "s-item__link"}, href=True)
            prices = table[0].find('span', {'class': 's-item__price'})
            p= prices.text

            remove = [f"{currency}", ","]
            for r in remove:
                p =p.replace(r, "")

            convert = c.convert(p, f'{currency}', 'USD')
            price = math.trunc(convert)

            if price < budget:
                print(f'{name.text} ---> Price:{price} USD ---> ' + link['href'])
                yep = True
            
            else:
                yep = False
                pass

            with open('products.csv', "a+", newline='') as f:
                w = csv.writer(f)
                w.writerow([f"{name.text}", f"{price}", f"{link['href']}", yep])

            f.close()


if __name__ == '__main__':

    with open('products.csv', "a+", newline='') as File:
        w = csv.writer(File)
        w.writerow(["Product", "Price", "Link", "Worth?"])
        w.writerow([" "])
    File.close()

    finder(currency, budget, url)