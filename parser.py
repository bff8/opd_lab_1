from bs4 import BeautifulSoup
import requests


def parse():
    url = 'https://auto.ru/omsk/cars/all/?sort=cr_date-desc'
    page = requests.get(url)
    page.encoding = 'utf8'

    print(page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    block = soup.findAll('div', class_='ListingItem')

    description = ''
    for data in block:
        name = data.find('a', class_='Link ListingItemTitle__link').text
        car_spec = data.find('div', class_='ListingItemTechSummaryDesktop__cell').text
        price = data.find('div', class_='ListingItem__priceBlock').text.split('₽')[0] + '₽'
        year = data.find('div', class_='ListingItem__year').text
        km_age = data.find('div', class_='ListingItem__kmAge').text
        description += f'{name} | {car_spec} | {year} | {km_age} | {price}\n'

    with open('output.txt','w',encoding='utf-8') as f:
        f.write(description)
