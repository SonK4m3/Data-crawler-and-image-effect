## **BACKEND TASK**

## **Crawl images from Gettyimages**

Requirements

- Python 3+
- Python "Beautiful Soup" library
```
pip install bs4
```
- Python "requests" library
```
pip install requests
```

How to work
- Run following command for collecte image url in 5 pages from Gettyimages
```
python image_extract.py
```
- image url has saved in `.\gettyimages\image_data\` folder
- list all image in `image_data.json`
- list image following page i in `image_data_page_i.json`

## **GettyImages Crawler**
- `Namespace(dir='./GettyImages', file='image_data', start=1, number_of_pages=5)`
- Run following command for collecte image url from GettyImages
```
python main.py
```
- Run following command for help
```
python main.py -h
```
- we can change arguments
```
usage: main.py [-h] [--dir DIR] [--file FILE] [-st START] [-np NUMBER_OF_PAGES]

crawling images from Gettyimages

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR             output dir
  --file FILE           output file
  -st START, --start START
                        the start page for search
  -np NUMBER_OF_PAGES, --number-of-pages NUMBER_OF_PAGES
                        number of pages for search
```

## **Pinterest**



