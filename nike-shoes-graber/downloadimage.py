#! /usr/bin/env python3

import requests
from urllib.parse import urlparse

def requests_image(url, filename):
    r = requests.get(url)
    suffix_list = ['jpg','gif','png','tif','svg']
    path = urlparse(url).path
    name = path.split('/')[-1]
    suffix = name.split('.')[-1]
    if suffix in suffix_list and r.status_code == requests.codes.ok:
        file_name = filename + suffix
        with open(file_name, 'wb') as file:
            file.write(r.content)
        return True
    else:
        return False



def main():
    url = 'http://images2.nike.com/is/image/DotCom/PDP_HERO/875943_300_B_PREM/air-max-90-ultra-2-flyknit-shoe.jpg'
    requests_image(url)

if __name__ == '__main__':
    main()
