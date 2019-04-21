# Get the current price of 10-gram gold bar from the bank site and compare it with the purchase price
import requests
from bs4 import BeautifulSoup as bs
import xlrd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

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

# Download the first xls file in the files list
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

# Retrieve the current gold bar value from the necessary cell of the first sheet
    open('gold.xls', 'wb').write(raw_file.content)
    book = xlrd.open_workbook("gold.xls", encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    new_price = int(sheet.cell_value(11, 3))

# Substract the current price from the purchase price and express it as percent
    old_price = 31341
    percentage = int(((new_price - old_price)*100)/old_price)
    print(f"{new_price} - 31341 = {int(new_price - old_price)} rub., {percentage}%")

# Write the date and the current price into a csv file
data = [{'date': date_from_link, 'old_price': old_price, 'new_price': new_price, 'percentage': percentage}]
with open("gold.csv", "a", encoding = "cp1251", newline = "") as f:
    fieldnames = ["date", "old_price", "new_price", "percentage"]
    writer = csv.DictWriter(f, fieldnames, delimiter = ";")
# If the date and the price are already in the file, skip it
    for row in data:
        if row in data:
            continue
        else:
            writer.writerow(row)
            
# Show the graphs with the current price value and the old price value (Jupyter) using data from csv file
    dataframe = pd.read_csv('gold.csv', sep=';')
    dataframe.drop_duplicates('date')
    plt.plot(dataframe['date'], dataframe['old_price'])
    plt.plot(dataframe['date'], dataframe['new_price'])
