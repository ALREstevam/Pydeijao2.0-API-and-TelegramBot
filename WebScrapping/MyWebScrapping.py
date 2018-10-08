import json
import re
import requests
from bs4 import BeautifulSoup


def find_indexes(alist, findFor):
    return [index for index, value in enumerate(alist) if value == findFor]


def text_clean(txt):
    txt = str(txt).replace('\r', '').replace('\\n', '').strip()
    return u'{}'.format(txt)


def text_remove(text, remove):
    return text.replace(remove, '')


class BandecoWebScrapper:
    def __init__(self, url = 'https://www.pfl.unicamp.br/Restaurante/view/site/cardapio.php'):
        self.url = url
        #self.url = 'cardapio.php.html'
        self.page = None
        self.soup = None

    def load_page(self):
        if self.url.startswith('http'):
            self.page = requests.get(self.url)
            self.soup = BeautifulSoup(self.page.content, 'lxml', from_encoding='utf-8')
        else:
            self.page = open(self.url, encoding='utf-8').read()
            self.soup = BeautifulSoup(self.page, 'lxml')

    def print_page(self):
        if self.page is None:
            self.load_page()
        print(self.soup.prettify())


    def extract_data(self):
        if self.page is None:
            self.load_page()

        page_title = text_clean(self.soup.find_all('p', class_='titulo')[0].get_text())
        food_hours = []
        foods = []

        for elem in self.soup.find_all('span', class_='titulo_cardapio'):
            food_hours.append(  text_clean(elem.get_text())  )

        for elem in self.soup.find_all('table', class_='fundo_cardapio'):
            txt = elem.get_text()

            txt = re.split(r'\n\n\n', txt)
            temp_foods = []
            for elem in txt:
                elem = re.sub(r'(\n\s*)', '', elem)
                elem = re.sub(r'\s*:', ':', elem)
                elem = re.sub(r':\s*', ':', elem)
                elem = re.sub(r'\n', '', elem)


                temp_foods.append(text_clean(elem))

                if elem.startswith('Observações'):
                    foods.append( temp_foods )
                    temp_foods = []

                elif elem == 'NÃO HÁ CARDÁPIO CADASTRADO!':
                    foods.append(['#no_food#:NÃO HÁ CARDÁPIO CADASTRADO'])
                    temp_foods = []
        jsonformat = {
            'title':page_title.split(' - ')[0],
            'date':page_title.split(' - ')[1].split(' (')[0],
            'weekDay':page_title.split(' (')[1].replace(')', ''),

            'foodRegister': {
            }
        }

        for i in range(len(food_hours)):
            type = food_hours[i]
            typefoods = foods[i]

            jsonformat['foodRegister'][type] = []

            count = 0
            for food in typefoods:
                splitted_food = food.split(':')

                if len(splitted_food) == 1:
                    splitted_food = ['food#{}#{}'.format(i, splitted_food[0]).replace(' ', '_'), splitted_food[0]]

                if splitted_food[1] == '-':
                    splitted_food[1] = ''

                jsonformat['foodRegister'][type].append( (splitted_food[0], splitted_food[1]) )
                count += 1
        return jsonformat

    def extract_data_to_json(self):
        return bytes(json.dumps(self.extract_data()), 'ascii').decode('unicode-escape')



