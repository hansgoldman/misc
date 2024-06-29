import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm


class EminenceSpecsScraper:
    def __init__(self):
        self.base_url = 'https://eminence.com/collections/guitar/products/'
        self.speakers = [
            'the_governor',
            'ramrod',
            'dv-77-16-12-mick-thomson-signature-speaker-16-ohm',
            'dv-77-12-mick-thomson-signature-speaker',
            'the_governor_16',
            '820h',
            'ga10-sc64-10-guitar-speaker-16-ohm',
            'ragin-cajun-10-guitar-speaker-16-ohm',
            'legend_em12n',
            'ga10_sc59',
            'ga_sc59',
            'double_t_15',
            'guit_fiddle',
            'cannabis_rex_10',
            'the_wizard',
            'the_tonker',
            'the_copperhead',
            'texas_heat_4',
            'texas_heat_16',
            'texas_heat',
            'swamp_thang_16',
            'swamp_thang',
            'screamin_eagle_16',
            'red-_white_and_blues',
            'ragin_cajun',
            'private_jack_16',
            'pf_400',
            'pf_350',
            'man_o_war',
            'lil_texas',
            'lil_buddy',
            'legend_v128',
            'legend_v1216',
            'legend_gb128',
            'legend_em12',
            'legend_1518',
            'legend_1275',
            'legend_1258',
            'legend_1218',
            'legend_1058',
            'ga10_sc64',
            'ga_sc64',
            'double_t_12',
            'cv-7516',
            'cv-75',
            'cannabis_rex_16',
            'cannabis_rex',
            '620h',
            'legend_1028k',
        ]

    def scrape(self):
        results = []

        for speaker in tqdm(self.speakers):
            url = self.base_url + speaker
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = self.parse_page(soup)

                results.extend(items)
            else:
                print(f"Failed to retrieve data for {speaker}")

        self.save_to_csv(results)

    def parse_page(self, soup):
        specs_table = soup.find('table', id='em-detail')
        speaker_name = soup.find('h1', class_='product-single__title').text.strip()

        items = []

        specs = {
            'Speaker': speaker_name,
        }

        if specs_table:
            rows = specs_table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if columns and len(columns) == 2:
                    label = columns[0].get_text(strip=True)
                    value = columns[1].get_text(strip=True).replace("\xa0", " ")

                    if label:a
                        specs[label] = value

        items.append(specs)

        return items

    def save_to_csv(self, data):
        keys = set().union(*(row.keys() for row in data))

        with open('eminence_speakers.csv', 'w', newline='', encoding='utf-8') as file_handle:
            writer = csv.DictWriter(file_handle, quotechar='"', fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


# Instantiate and run the scraper
if __name__ == '__main__':
    scraper = EminenceSpecsScraper()
    scraper.scrape()
