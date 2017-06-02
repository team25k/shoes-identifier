#! /usr/bin/env python3

import requests
import os
import sys
import re
import json
from downloadimage import requests_image


class Color_Shoe:
    def __init__(self, data, category, name_shoe):
        self.images = []
        self.colores = []
        self.data = data

        r = requests.get(data['pdpUrl'])

        pattern_container = re.compile('exp-pdp-image-container.*\\n.*\\n.*data-large-image="(.*)"', re.MULTILINE)
        matches = pattern_container.finditer(r.text)
        if matches is None:
            return
        self.images = [m.group(1) for m in matches]

        index = 0
        path = createShoesDir(category, data['colorDescription'])
        for imageurl in self.images:
            requests_image(imageurl, path + '/' + name_shoe + '_' + str(index))
            index += 1
        
        



class Shoe:
    def __init__(self, data, category):
        self.images = []
        self.colores = []
        self.data = data

        r = requests.get(data['pdpUrl'])

        pattern_container = re.compile('exp-pdp-image-container.*\\n.*\\n.*data-large-image="(.*)"', re.MULTILINE)
        matches = pattern_container.finditer(r.text)
        if matches is None:
            return
        self.images = [m.group(1) for m in matches]

        index = 0
        path = createShoesDir(category, self.data['title'])
        for imageurl in self.images:
            requests_image(imageurl, path + '/' + self.data['title'] + '_' + str(index))
            index += 1
            
        if data['colorways'] is not None:
            for color in data['colorways']:
                self.colores.append(Color_Shoe(color, path, data['title']))

            

    def print(self):
        print(self.name)
        print(self.color)
        print(self.price)
        print(self.image)
        print()

def createShoesDir(category_name, title):
    duplicate = 0
    if title is None:
        title = 'none'
    temp_path = category_name + '/' +  title
    path = temp_path
    while os.path.exists(path):
        path = temp_path + str(duplicate)
        duplicate += 1
    os.mkdir(path)
    return path


def category(url, category_name):
    os.mkdir(category_name)
    shoes = []
    pn = 1
    while True:
        r = requests.get(url.format(pn=pn))
        pretty = json.loads(r.text)

        if not pretty['foundResults']:
            break

        pn += 1

        for section in pretty['sections']:
            for product in section['products']:
                print(product['title'])
                # print(product['localPrice'])
                shoe = Shoe(product, category_name)
                shoes.append(shoe)
                # shoe.saveShoes(category_name);
                # for colorway in product['colorways']:
            # shoe = Shoe(grid.group(1))
            # if shoe.exists:
            #     lis.append(shoe)
            #     shoe.print()
            #typename += 1
            #print(str(typename) + "----------------------------------------------------------")
    return len(shoes)


def main():

    number_mans = category("http://store.nike.com/html-services/gridwallData?country=CA&lang_locale=en_GB&gridwallPath=mens-shoes/7puZoi3&pn={pn}", 'man')

    number_womens = category("http://store.nike.com/html-services/gridwallData?country=CA&lang_locale=en_GB&gridwallPath=womens-shoes/7ptZoi3&pn={pn}",'women') 
    
    number_boys = category("http://store.nike.com/html-services/gridwallData?country=CA&lang_locale=en_GB&gridwallPath=boys-shoes/7pvZoi3&pn={pn}", 'boys') 

    number_girls =  category("http://store.nike.com/html-services/gridwallData?country=CA&lang_locale=en_GB&gridwallPath=girls-shoes/7pwZoi3&pn={pn}", 'girls')

    s = number_girls + number_boys + number_mans + number_girls
    print(s)


if __name__ == '__main__':
    main()
