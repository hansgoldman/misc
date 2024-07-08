import requests
from bs4 import BeautifulSoup

def scrape_products(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        div_class = 'one-third one-whole-mob column thumbnail thumbnail-hover-enabled--false medium-down--one-half'
        product_list_items = soup.find_all('div', class_=div_class)

        for item in product_list_items:
            # Extract product link
            product_link = item.find('a', class_='product-info__caption')['href']

            # Print the product URL
            print(product_link)

    else:
        raise Exception(f'Error: Could not load the page. Status Code: {response.status_code}')

# URL of the WGS speakers products page
urls = [
    'https://wgsusa.com/collections/speakers',
]

# Call the function to scrape and print product URLs
for url in urls:
    scrape_products(url)
