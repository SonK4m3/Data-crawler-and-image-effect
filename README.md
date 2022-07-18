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
- list image folowwing page i in `image_data_page_i.json`
