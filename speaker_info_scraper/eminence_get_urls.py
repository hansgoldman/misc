from bs4 import BeautifulSoup
import requests


class ProductLinkScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_product_links(self):
        product_links = []
        current_page  = 1

        while True:
            url      = f"{self.base_url}?page={current_page}"
            response = requests.get(url)
            soup     = BeautifulSoup(response.content, 'html.parser')
            divs     = soup.select('div.grid-view-item.product-card')

            if not divs:
                break  # Exit loop if no more product cards are found

            for div in divs:
                link = div.find('a', class_='grid-view-item__link grid-view-item__image-container full-width-link')

                if link:
                    href         = link.get('href')
                    product_name = href.split('/')[-1]  # Extract the part after '/products/'

                    product_links.append(product_name)

            current_page += 1

        return product_links


if __name__ == '__main__':
    base_url      = 'https://eminence.com/collections/guitar'
    scraper       = ProductLinkScraper(base_url)
    product_links = scraper.scrape_product_links()

    for link in product_links:
        if link != 'xtc112_bt':
            print(f"            '{link}',")
