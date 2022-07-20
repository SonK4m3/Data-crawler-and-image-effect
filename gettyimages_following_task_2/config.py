try:
    import urllib
except Exception as e:
    print('Caught exception while importing: {}'.format(e))


class Config:
    IMAGE_SEARCH_URL = 'https://www.gettyimages.com/photos/oscars?assettype=image&family=editorial&phrase=oscars&sort=mostpopular&&page={}'
    BASE_URL = 'https://www.gettyimages.com'
    BASE_DIR = './gettyimage'

    def __init__(self, save_dir="", save_file="", start=1, number=5):
        self.save_dir = save_dir
        self.save_file = save_file
        self.start = start
        self.number = number
    
    #image search url
    @property
    def search_url(self):
        return self.IMAGE_SEARCH_URL
    
    @property
    def base_url(self):
        return self.BASE_URL

    @property
    def image_data(self):
        return '{"option":{"save_dir":"' + self.save_dir + '","save_file":"' + self.save_file + '","start":"' + str(self.start) + '","number":"' + str(self.number) + '"}'