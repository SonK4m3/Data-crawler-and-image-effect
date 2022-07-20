try:
    import os
    import argparse
    from GettyimagesScraper import Scraper 
    from config import Config
except Exception as e:
    print("Caught exception while importing: {}".format(e))

    
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawling images from Gettyimages')
    parser.add_argument('--dir', help='output dir', default='./GettyImages', type=str)
    parser.add_argument('--file', help='output file', default='image_data', type=str)
    parser.add_argument('-st', '--start', help="the start page for search", default=1, type=int)
    parser.add_argument('-np', '--number-of-pages', help='number of pages for search', default=5, type=int )
    args = parser.parse_args()

    print(args)

    print("start crawling...")

    configs = Config(save_dir= args.dir, save_file= args.file, start= args.start, number= args.number_of_pages)

    crawler = Scraper(configs)

    crawler.image_crawler