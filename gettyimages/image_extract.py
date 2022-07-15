try:
    from bs4 import BeautifulSoup
    import requests
    import re
    import bs4
    import os
    import json
    import time
    import cv2
    import mediapipe as mp

    import random
    from html import unescape
    import traceback
except Exception as e:
    print('Caught exception while importing: {}'.format(e))

BASE_URL = 'https://www.gettyimages.com'
BASE_DIR = './gettyimage'

IMAGE_LIST = 'https://www.gettyimages.com/photos/oscars?assettype=image&family=editorial&phrase=oscars&sort=mostpopular&page={}'
IMAGE_SAVE_DIR = BASE_DIR + '/image_data'

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def image_extract(url=IMAGE_LIST, save_dir=IMAGE_SAVE_DIR, start=1):

    make_dir(save_dir)

    url = url.format(start)
    soup = request_url(url)

    elements = soup.select('div.MosaicAsset-module__galleryMosaicAsset____wxTl article ')

    data = []
    for ele in elements:
        try:
            link = ele.select('a figure picture img')[0]
            img = link['src']
            
            # print(href)
            # print('-----\n\n')
 
            ele_data = {
                'url' : img,
                'page' : start
            }
            
            print(ele_data)

            data.append(ele_data)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    filename = 'image_page{}.json'.format(start)
    write_json(save_dir + '/' + filename, data)

def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_image_list(page_number = 1):
    try:
        filename = IMAGE_SAVE_DIR + '/' + 'image_page{}.json'.format(page_number)
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print('Error loading {}'.format(filename), e)
        traceback.print_exc()
        return []


def req_url(url):
    session = requests.Session()

    my_headers = {"User-Agent" : 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114\
                Safari/537.36\
                Edg/103.0.1264.49",
                "Accept" : "text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8"}
    response = session.get(url, headers=my_headers)
    return response

def request_url(url):
    session = requests.Session()

    my_headers = {"User-Agent" : 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114\
                Safari/537.36\
                Edg/103.0.1264.49",
                "Accept" : "text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,image/apng,*/*;q=0.8"}
    response = session.get(url, headers=my_headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

if __name__ == '__main__':
    for i in range(1, 6): 
        image_extract(start=i)