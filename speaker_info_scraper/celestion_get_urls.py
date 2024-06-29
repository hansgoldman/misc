import requests
from bs4 import BeautifulSoup

def scrape_products(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        product_list_items = soup.find_all('li', class_='product')
        
        for item in product_list_items:
            product_link = item.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')['href']
            product_slug = product_link.split('/')[-2]  # Get the second-to-last part of the URL
            print(f"            '{product_slug}',")
    else:
        raise Exception(f'Error: Could not load the page. Status Code: {response.status_code}')

# URL of the guitar speakers products page
urls = [
    'https://celestion.com/products/?fwp_product_catalogue=guitar-loudspeakers',
    'https://celestion.com/products/?redirect=1&redirect=1&redirect=1&fwp_product_catalogue=guitar-loudspeakers&fwp_paged=2',
    'https://celestion.com/products/?redirect=1&redirect=1&redirect=1&fwp_product_catalogue=guitar-loudspeakers&fwp_paged=3',
]

# Call the function to scrape and print product slugs
for url in urls:
    scrape_products(url)
