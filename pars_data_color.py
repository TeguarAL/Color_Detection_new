import requests
import csv
from bs4 import BeautifulSoup as bs

url = requests.get("https://colorscheme.ru/color-names.html")
soup = bs(url.content, 'html.parser')

filename = "color_data_base.csv"
csv_writer = csv.writer(open(filename, 'w', encoding='utf-8'))

for tr in soup.find_all("tr"):
    data = []
    for th in tr.find_all("th"):
        data.append(th.text)
    if data:
        print("Inserting headers : {}".format(','.join(data)))
        csv_writer.writerow(data)
        continue

    for td in tr.find_all("td"):
        if td.a:
            data.append(td.a.text.strip())
        else:
            data.append(td.text.strip())
    if data:
        print("Inserting data: {}".format(','.join(data)))
        csv_writer.writerow(data)
