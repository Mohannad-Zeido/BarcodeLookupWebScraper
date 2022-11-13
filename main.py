import time

from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask, request

from Model.product import Product
from Model.product import ProductEncoder


def get_product_from_website(barcode):

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(options=chrome_options)
    url = "https://www.barcodelookup.com/" + barcode
    print(url)
    try:
        driver.get(url)
        page_source = driver.page_source
        time.sleep(1)
        driver.quit()
    except Exception as ex:
        driver.quit()
        return Product(str(ex), barcode, "", "")

    soup = BeautifulSoup(page_source, 'html.parser')

    if "bad barcode" in soup.find("title").text.lower():
        return Product("bad barcode", barcode, "", "")
    if "not found" in soup.find("title").text.lower():
        return Product("not found", barcode, "", "")

    section = soup.find('section', attrs={'class': None, 'id': None})

    image_div = section.find('div', attrs={'id': "largeProductImage"})
    image_src = image_div.find('img').get('src')

    product_details = section.find('div', attrs={'class': "product-details"})
    product_name = product_details.find('h4').text.strip()

    product_text_labels = product_details.find_all('div', attrs={'class': "product-text-label"})
    category = ""
    for pl in product_text_labels:
        if "category" in pl.text.lower():
            a = pl.find_next('span', attrs={'class': "product-text"})
            category = a.text.strip()
    print(product_name)
    print(image_src)
    print(category)

    return Product(product_name, barcode, image_src, category)


app = Flask(__name__)


@app.route('/lookup', methods=['GET'])
def get_product():
    dsa = request.args
    p = get_product_from_website(dsa["barcode"])

    return ProductEncoder().encode(p)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1234, debug=True)
