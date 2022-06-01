import requests
import pprint
import csv
from bs4 import BeautifulSoup


def find(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('div', class_='living-list-card__main-container')
    return tags


def make_character_list(tags):
    apartments = []
    for v1 in tags:
        # print(v1)
        apartment = {}

        def search(apartment_type, blok_type, link):
            try:
                tags = v1.find(blok_type, class_=link)
                apartment[apartment_type] = tags.text
            except AttributeError:
                apartment[apartment_type] = ''

        search('Адрес', 'a', 'link')
        search('Район', 'div', 'search-item-district living-list-card__inner-block')
        search('Город', 'div',
               'living-list-card__city-with-estate living-list-card-city-with-estate living-list-card__inner-block')
        search('Площадь', 'div', 'living-list-card__area living-list-card-area living-list-card__inner-block')
        search('Этажность', 'div', 'living-list-card__floor living-list-card-floor living-list-card__inner-block')
        search('Материал', 'div', 'living-list-card__material living-list-card-material living-list-card__inner-block')
        search('Цена', 'div', 'living-list-card-price__item _object')
        apartment['Цена'] = apartment['Цена'].replace(chr(160), ' ') + 'руб'
        apartments.append(apartment)
    return apartments


def print_to_console(apartments):
    for i in apartments:
        print('=' * 60)
        pprint.pprint(i)


def save_to_file(apartments):
    title = ['Город', 'Район', 'Адрес', 'Площадь', 'Этажность', 'Материал', 'Цена']
    with open("Apartaments.csv", mode="w", encoding='utf-8', newline='') as w_file:
        f = csv.writer(w_file, delimiter="\t")
        f.writerow(title)
        for d in apartments:
            # print( d['Район'], d['Город'], d['Адрес'], d['Материал'] )
            f.writerow([d['Город'], d['Район'], d['Адрес'], d['Площадь'], d['Этажность'], d['Материал'], d['Цена']])


if __name__ == '__main__':
    tags = find('https://ufa.n1.ru/kupit/kvartiry/')
    apartments = make_character_list(tags)
    print_to_console(apartments)
    save_to_file(apartments)
