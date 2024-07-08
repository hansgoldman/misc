import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm


class SpecsScraper:
    def __init__(self):
        self.base_url = 'https://wgsusa.com/collections/speakers/products/'

        self.speakers = [
            '12-et65-65-watts',
            '8-g8c-20-watts',
            '12-veteran-30-60-watts',
            '10-veteran-20-watts',
            '12-g12c-s-75-watts',
            '12-invader-50-50-watts',
            '12-retro-30-75-watts',
            '12-reaper-hp-50-watts',
            '12-green-beret-25-watts',
            '12-g12c-75-watts',
            '12-et90-90-watts',
            '10-et10-65-watts',
            '10-g10c-75-watts',
            '12-g12q-20-watts',
            '12-reaper-30-watts',
            '10-g10c-s-75-watt',
            '10-green-beret-25-watts',
            '8-g8a-alnico-20-watts',
            '12-wgs12l-200-watts',
            '10-retro-10-60-watts',
            '12-blackhawk-alnico-50-watts',
            '15-g15c-75-watts',
            '12-g12a-alnico-75-watts',
            '10-g10a-75-watts',
            '12-black-blue-alnico-15-watts',
            '12-blackhawk-hp-alnico-100-watts',
            '15-g15a-alnico-75-watts',
        ]


    def scrape(self):
        results = []

        for speaker in tqdm(self.speakers):
            url = self.base_url + speaker
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = self.parse_page(soup, speaker)

                results.extend(items)
            else:
                print(f"Failed to retrieve data for {speaker}")

        self.save_to_csv(results)


    def parse_page(self, soup, speaker):
        specs_div      = soup.find('div', id='prod-specs')
        speaker_header = soup.find('h1', class_='product_name').text.strip()
        diameter       = speaker_header.split(' ')[0]
        wattage        = speaker_header.split(' - ')[-1]
        start_index    = len(diameter) + 1
        end_index      = len(speaker_header) - (len(wattage) + 3)
        speaker_name   = speaker_header[start_index:end_index]
        weight         = self.parse_speaker_weight(soup)
        mounting_specs = self.parse_mounting_specs(soup)
        impedances     = self.parse_impedences(soup)

        specs = {
            'Speaker': speaker_name,
            'Diameter': diameter,
            'Wattage': wattage,
            'Weight': weight,
            'Impedance': impedances,
            **mounting_specs
        }

        if specs_div:
            items = specs_div.find_all('div', style='display:flex')

            for item in items:
                label_element = item.find('p', style='width:50%;text-align:left')
                value_element = item.find('p', style='width:50%;text-align:right')

                if label_element and value_element:
                    label = label_element.text.strip().rstrip(':')
                    value = value_element.text.strip()
                    value = value.replace(' Surface Area of Cone (Sd):', '')

                    specs[label] = value
        else:
            print(f"Could not find 'prod-specs' div for {speaker}")

        return [specs]

    @staticmethod
    def parse_speaker_weight(soup):
        # Find the unit weight within the product description
        search_term     = 'Unit Weight: '
        unit_weight_tag = soup.find('p', string=lambda text: text and text.strip().startswith(search_term))
        unit_weight     = ''

        if unit_weight_tag:
            unit_weight_text  = unit_weight_tag.text.strip()
            unit_weight_value = unit_weight_text.replace(search_term, '')
            unit_weight       = unit_weight_value

            return unit_weight

    def parse_mounting_specs(self, soup):
        # Find the mounting information under the "one-whole column" class
        column_divs  = soup.find_all('div', class_='one-whole column')
        mounting_div = self.get_mounting_div(column_divs)

        mounting_specs = {
            'Diameter': '',
            'Overall depth': '',
            'Cut-out diameter': '',
            'Mounting slot dimensions': '',
            'Number of mounting slots': '',
            'Mounting slot PCD': '',
        }

        if mounting_div:
            lis = mounting_div.find_all('li')

            for li in lis:
                li_text = li.text.strip()

                # Try to find a matching key in mounting_specs
                matched_key = None

                for key in mounting_specs:
                    if li_text.startswith(key):
                        matched_key = key
                        break

                if matched_key:
                    value = li_text[len(matched_key):].strip().replace('”', '"')

                    if value.startswith(':'):
                        value = value[1:].strip()

                    mounting_specs[matched_key] = value

        return mounting_specs

    @staticmethod
    def get_mounting_div(column_divs):
        # Source HTML is sloppy, pages it's a <h2>; others are <p> and the capitalization changes depending
        mounting_div = None
        tag_types    = ['h2', 'p']
        search_term  = lambda x: x and x.lower()=='mounting information'

        for div in column_divs:
            tag = div.find(tag_types, string=search_term)
            if tag:
                mounting_div = div
                break

        return mounting_div

    @staticmethod
    def parse_impedences(soup):
        # Find the div with class 'swatch is-flex is-flex-wrap' which contains impedance options
        swatch_div = soup.find('div', class_='swatch is-flex is-flex-wrap')
        impedances_list = []

        if swatch_div:
            # Find all input elements inside the swatch_div
            input_elements = swatch_div.find_all('input')

            for input_elem in input_elements:
                # Extract the impedance value from the 'value' attribute of the input element
                impedance_value = input_elem.get('value')

                if impedance_value:
                    impedances_list.append(impedance_value.strip())

        impedances_string = ', '.join(impedances_list)
        impedances_string = impedances_string.replace(' ohm', 'Ω')

        return impedances_string

    @staticmethod
    def save_to_csv(data):
        keys = set().union(*(row.keys() for row in data))

        with open('wgs_speakers.csv', 'w', newline='', encoding='utf-8') as file_handle:
            writer = csv.DictWriter(file_handle, quotechar='"', fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


# Instantiate and run the scraper
if __name__ == '__main__':
    scraper = SpecsScraper()
    scraper.scrape()
