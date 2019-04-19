# Get the current price of 10-gram gold bar from the bank site and compare it with the purchase price
import requests
from bs4 import BeautifulSoup as bs
import xlrd
import csv
from datetime import datetime

# Open up the necessary page of the bank's site
def get_html(url):
# Secure from the non-operating site
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("сетевая ошибка")
        return False

html = get_html("http://data.sberbank.ru/moscow/ru/quotes/archivoms/?base=beta")

# Open the first file in the files list
if html:
    soup = bs(html, "html.parser")
    raw_script = soup.find("div", {'class': "layout-column"}).find('script').contents[0]
    raw_script = raw_script.split('url: "')[1].split('"')[0]
    link = "http://sberbank.ru" + raw_script
    raw_file = requests.get(link, allow_redirects=True)

# Get the date from the link for further analysis
    date_from_link = link.split("/dm")[1][:6]
    date_from_link = datetime.strptime(date_from_link, '%d%m%y')
    date_from_link = datetime.date(date_from_link)
    print(date_from_link)

# Retrieve value from the first sheet and the necessary cell
    open('gold.xls', 'wb').write(raw_file.content)
    book = xlrd.open_workbook("gold.xls", encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    new_price = int(sheet.cell_value(11, 3))

# Substract the new price from the purchase price and express it as percent
    old_price = 31341
    percentage = int(((new_price - old_price)*100)/old_price)
    print(f"{new_price} - 31341 = {int(new_price - old_price)} rub., {percentage}%")

data = [{'date': date_from_link, 'old_price': old_price, 'new_price': new_price, 'percentage': percentage}]
with open("gold.csv", "a", encoding = "cp1251", newline = "") as f:
    fieldnames = ["date", "old_price", "new_price", "percentage"]
    writer = csv.DictWriter(f, fieldnames, delimiter = ";")
    #writer.writeheader()
    for row in data:
        writer.writerow(row)

# Matplotlib