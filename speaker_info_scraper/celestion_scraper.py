import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm


class SpecsScraper:
    def __init__(self):
        self.base_url = 'https://celestion.com/product/'

        self.speakers = [
            'foxhall',
            'celestion-100',
            'celestion-blue',
            'celestion-ruby',
            'celestion-cream',
            'celestion-gold',
            'celestion-g10-gold',
            'g12m-greenback',
            'g12h-anniversary',
            'g10-greenback',
            'g12-evh',
            'g12m-65-creamback',
            'g12h-75-creamback',
            'neo-creamback',
            'g10-creamback',
            'vintage-30',
            'heritage-series-g12-65',
            'g12m-50-hempback',
            'g10-vintage',
            'neo-copperback',
            'g12t-75',
            'classic-lead',
            'g12h-150-redback',
            'v-type',
            'vt-junior',
            'a-type',
            'neo-v-type',
            'g15v-100-fullback',
            'midnight-60',
            'ten-30',
            'eight-15',
            'seventy-80',
        ]


    def scrape(self):
        results = []

        for speaker in tqdm(self.speakers):
            url      = self.base_url + speaker
            response = requests.get(url)

            if response.status_code == 200:
                soup  = BeautifulSoup(response.content, 'html.parser')
                items = self.parse_page(soup)

                results.extend(items)
            else:
                print(f"Failed to retrieve data for {speaker}")

        self.save_to_csv(results)


    def parse_page(self, soup):
        product_detail_lines = soup.find_all('div', class_='product-detail-spec-col-line')
        speaker_name         = soup.find('h1', id='product-detail-title').text.strip()
        items                = []

        specs = {
            'Speaker': speaker_name,
        }

        for line in product_detail_lines:
            label = line.find('div', recursive=False).get_text(strip=True)
            value = line.find('div', recursive=False).find_next_sibling('div').get_text(strip=True)

            if label == 'Power rating':
                value = value.replace('Up to ', '')

            specs[label] = value

        items.append(specs)

        return items


    def save_to_csv(self, data):
        keys = set().union(*(row.keys() for row in data))

        with open('celestion_speakers.csv', 'w', newline='', encoding='utf-8') as file_handle:
            writer = csv.DictWriter(file_handle, quotechar='"', fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


# Instantiate and run the scraper
if __name__ == '__main__':
    scraper = SpecsScraper()
    scraper.scrape()
