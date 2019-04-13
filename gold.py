# Взять текущую стоимость 10 гр. золотого слитка с сайта Сбербанка и сравнить её со стоимостью покупки
import requests
from bs4 import BeautifulSoup as bs
import openpyxl
import xlrd

# Зайти на нужную страницу Сбербанка
def get_html(url):
# Подстраховаться от неработающего сервиса
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("сетевая ошибка")
        return False

# Зайти на страницу Сбербанка с архивом курсов драгоценных металлов
html = get_html("http://data.sberbank.ru/moscow/ru/quotes/archivoms/?base=beta")

# Open the first file in the list
if html:
    soup = bs(html, "html.parser")
    print(type(soup))
    raw_script = soup.find("div", {'class': "layout-column"}).find('script').contents[0]
    raw_script = raw_script.split('url: "')[1].split('"')[0]
    link = "http://sberbank.ru" + raw_script
    raw_file = requests.get(link, allow_redirects=True)
    open('gold.xls', 'wb').write(raw_file.content)


# Retrieve value from D12 cell
book = xlrd.open_workbook("gold.xls", encoding_override="cp1252")
new_price = int(book['D12'].value) 
print(new_price)

#Вычесть из этой суммы сумму покупки 31341
old_price = 31341
price_difference = new_price - old_price

#Выразить разницу в процентах
percentage = (price_difference*100)/price_old
print(f"{price_difference} руб., {percentage}%")

# Matplotlib
# Database