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
IMAGE_SAVE_FILE = 'image_data'

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def image_extract(url=IMAGE_LIST, save_dir=IMAGE_SAVE_DIR, save_file = IMAGE_SAVE_FILE, start=1):

    make_dir(save_dir)

    url = url.format(start)
    soup = request_url(url)

    elements = soup.select('div.MosaicAsset-module__galleryMosaicAsset____wxTl article')

    data = []
    for ele in elements:
        try:
            link = ele.select('a figure picture img')[0]
            img = link['src']
 
            ele_data = {
                'url' : img,
                'page' : start
            }
            
            data.append(ele_data)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    #write list image page
    filename = save_file + '_page_{}.json'.format(start)
    write_json(save_dir + '/' + filename, data)

    #write list all image        
    filename = save_file + '.json'
    rewrite_json(save_dir + '/' + filename, data)

def write_json(filename, data):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_json(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print('Error loading {}'.format(filename), e)
        traceback.print_exc()
        return []

def rewrite_json(filename, data):
    new_data = read_json(filename)
    new_data = new_data + data
    write_json(filename,data)

def get_all_image():
    filename = IMAGE_SAVE_DIR + '/' + IMAGE_SAVE_FILE + '.json'
    data = read_json(filename)
    return data

def get_image_list(page_number = 1):
    filename = IMAGE_SAVE_DIR + '/' + IMAGE_SAVE_FILE + '_page_{}.json'.format(page_number)
    data = read_json(filename)
    return data

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

def image_crawler(url=IMAGE_LIST, save_dir=IMAGE_SAVE_DIR, save_file=IMAGE_SAVE_FILE, start=1, number=5):
    for i in range(start, start + number + 1):
        image_extract(url,save_dir,save_file,i)

if __name__ == '__main__':
    image_crawler()