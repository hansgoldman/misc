import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm


class JensenSpecsScraper:
    def __init__(self):
        self.base_url = 'https://www.jensentone.com/'
        self.speakers = [
            'vintage-alnico/p6v',
            'vintage-alnico/p8r',
            'vintage-alnico/p10r',
            'vintage-alnico/p10r-fen',
            'vintage-alnico/p10q',
            'vintage-alnico/p12r',
            'vintage-alnico/p12q',
            'vintage-alnico/p12n',
            'vintage-alnico/p12n-no-bell',
            'vintage-alnico/p15n-no-bell',
            'vintage-ceramic/c6v',
            'vintage-ceramic/c8r',
            'vintage-ceramic/c10r',
            'vintage-ceramic/c10q',
            'vintage-ceramic/c12r',
            'vintage-ceramic/c12q',
            'vintage-ceramic/c12n',
            'vintage-ceramic/c12k',
            'vintage-ceramic/c12k-2',
            'vintage-ceramic/c15n',
            'vintage-ceramic/c15k',
            'vintage-neo/n12k',
            'jet-series/8-falcon-8',
            'jet-series/10-falcon-40',
            'jet-series/10-blackbird-40',
            'jet-series/10-electric-lightning-50',
            'jet-series/10-silverbird-10',
            'jet-series/10-blackbird-100',
            'jet-series/10-tornado-classic-100',
            'jet-series/12-blackbird-40',
            'jet-series/12-falcon-50',
            'jet-series/12-tornado-stealth-65',
            'jet-series/12-electric-lightning-70',
            'jet-series/12-silverbird-12',
            'jet-series/12-nighthawk-75',
            'jet-series/12-tornado-stealth-80',
            'jet-series/12-blackbird-100',
            'jet-series/12-tornado-classic-100',
            'jet-series/12-tornado-stealth-100',
            'jet-series/12-raptor-100',
            'mod-series/mod-5-30',
            'mod-series/mod-6-15',
            'mod-series/mod-8-20',
            'mod-series/mod-10-35',
            'mod-series/mod-10-50',
            'mod-series/mod-10-70',
            'mod-series/mod-12-35',
            'mod-series/mod-12-50',
            'mod-series/mod-12-70',
            'mod-series/mod-12-110',
            'd-series/c12d',
            'd-series/n12d',
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
        specs_tables = soup.find_all('table', class_='table table-bordered table-condensed table-hover table-striped')
        speaker_name = soup.find('h1', class_='page-header').text.strip()
        items        = []

        specs = {
            'Speaker': speaker_name,
        }

        if specs_tables:
            for table in specs_tables:
                rows = table.find_all('tr')

                for row in rows:
                    columns = row.find_all(['th', 'td'])

                    if columns and len(columns) >= 2:
                        label      = columns[0].get_text(strip=True)
                        value_list = list(filter(len, [cell.get_text(strip=True) for cell in columns[1:]]))
                        value_list = []

                        skip_values = set([
                            'RE',
                            'ƒS',
                            'QMS',
                            'QES',
                            'QTS',
                            'MMS',
                            'CMS',
                            'BxL',
                            'VAS',
                            'XMAX',
                            'nO',
                            'SD',
                            'RES',
                            'LE',
                            '',
                        ])

                        for cell in columns[1:]:
                            cell = cell.get_text(strip=True)

                            if cell not in skip_values:
                                value_list.append(cell)

                        value_set = set(value_list)
                        
                        # Check if all the values are the same, just repeated for different impedences
                        # If so, let's not repeat data
                        if len(value_set) == 1:
                            value = value_list[0]
                        else:
                            value = ', '.join(value_list)

                        if label:
                            specs[label] = value

        items.append(specs)
        #for item in items:
        #    for key, value in item.items():
        #        print(key, '=', value)

        return items


    def save_to_csv(self, data):
        keys = set().union(*(row.keys() for row in data))

        with open('jensen_speakers.csv', 'w', newline='', encoding='utf-8') as file_handle:
            writer = csv.DictWriter(file_handle, quotechar='"', fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


# Instantiate and run the scraper
if __name__ == '__main__':
    scraper = JensenSpecsScraper()
    scraper.scrape()
