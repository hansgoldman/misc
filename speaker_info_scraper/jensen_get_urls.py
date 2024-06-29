from bs4 import BeautifulSoup
import requests


class ProductLinkScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape_product_links(self):
        product_links = []

        url_endings = [
            'vintage-alnico',
            'vintage-ceramic',
            'vintage-neo',
            'jet-series',
            'mod-series',
            'd-series',
        ]

        for url_ending in url_endings:
            url      = f"{self.base_url}{url_ending}"
            response = requests.get(url)
            soup     = BeautifulSoup(response.content, 'html.parser')
            rows     = soup.find_all('tr')

            for row in rows:
                link = row.find('a')

                if link:
                    href = link.get('href')

                    if href.startswith('/'):
                        href = href[1:]

                    product_links.append(href)

        return product_links


if __name__ == '__main__':
    base_url      = 'https://www.jensentone.com/'
    scraper       = ProductLinkScraper(base_url)
    product_links = scraper.scrape_product_links()

    skip_products = set([
        'vintage-alnico/bell-cover-alnico-r-and-q-types',
        'vintage-alnico/bell-cover-alnico-n-types',
        'speakers/gaskets',
        'jet-series/bell-cover-blackbirds',
    ])

    for link in product_links:
        if link not in skip_products:
            print(f"            '{link}',")
