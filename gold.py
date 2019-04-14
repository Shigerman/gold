# Get the current price of 10-gram gold bar from the bank site and compare it with the purchase price
import requests
from bs4 import BeautifulSoup as bs
import openpyxl
import xlrd

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
    open('gold.xls', 'wb').write(raw_file.content)

# Retrieve value from the first sheet and the necessary cell
    book = xlrd.open_workbook("gold.xls", encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    new_price = int(sheet.cell_value(11, 3))

# Substract the new price from the purchase price and express it as percent
    percentage = ((new_price - 31341)*100)/31341
    print(f"{new_price} - 31341 = {int(new_price - 31341)} rub., {int(percentage)}%")

# Matplotlib
# Database