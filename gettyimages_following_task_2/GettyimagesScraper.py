try:
    from bs4 import BeautifulSoup
    import requests
    import bs4
    import os
    import json
    import traceback
except Exception as e:
    print('Caught exception while importing: {}'.format(e))


def make_dir(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

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

class Scraper:
    def __init__(self, config, image_urls = []):
        self.config = config
        self.image_urls = image_urls

    def image_extract(self, start=1):
        //setting config before crawl
        url = self.config.IMAGE_SEARCH_URL
        save_dir = self.config.save_dir
        save_file = self.config.save_file

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
        # filename = save_file + '.json'
        # rewrite_json(save_dir + '/' + filename, data)  
    
    @property
    def image_crawler(self):
        
        start = self.config.start
        number = self.config.number

        result = None

        for i in range(start, start + number):
            self.image_extract(start=i)
            # print(i)
