import csv
from datetime import date
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import textwrap
import xlrd
from typing import Union


def get_current_date() -> str:
    current_date = date.today() # 07.11.2020
    return current_date.strftime('%d.%m.%Y')


def get_current_month(current_date: str) -> int:
    return int(current_date[3:5]) - 1 # months start from 0


def get_current_year(current_date: str) -> int:
    return int(current_date[6:10])


def compile_bank_url(current_month: int, current_year: int) -> str:
    url_start = "https://www.sberbank.ru/proxy/services/dict-services/"\
                "document/list?groupCode=279&regionCode=77&month="
    return url_start + str(current_month) + '&year=' + str(current_year)


def get_bank_url_content(current_month: int, current_year: int) -> bytes:
    url = compile_bank_url(current_month, current_year)
    try:
        result = requests.get(url)
        return result.content
    except(requests.RequestException, ValueError):
        raise Exception("network error")


def download_file_with_prices(url_content: bytes) -> bytes:
    most_recent_file_available = json.loads(url_content)[-1]
    most_recent_file_url = most_recent_file_available['fileUrl']
    most_recent_file_url = 'http://sberbank.ru' + most_recent_file_url
    file_content = requests.get(most_recent_file_url, allow_redirects=True)
    return file_content.content


def get_gold_bar_price_from_xls(xls_file_name: str) -> int:
    book = xlrd.open_workbook(xls_file_name, encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    return int(sheet.cell_value(11, 3))


def main():
    current_date = get_current_date()
    current_month = get_current_month(current_date)
    current_year = get_current_year(current_date)
    url_content = get_bank_url_content(current_month, current_year)

    min_content_size = 3 # '[]' for empty response
    min_year_to_check = 2018
    while len(url_content) < min_content_size and \
        current_year >= min_year_to_check:
        # check previous months if bank has no prices for current month
        if current_month > 0:
            current_month -= 1
        elif current_month == 0:
            current_month = 11
            current_year -= 1
        url_content = get_bank_url_content(current_month, current_year)

    xls_file_name = 'gold.xls'
    if url_content:
        file_content = download_file_with_prices(url_content)
        with open(xls_file_name, 'wb') as out:
            out.write(file_content)
    else:
        print("File with gold bar prices was not found")
    

    def save_new_price_to_make_a_graph():
        date_list: list = []
        with open("gold.csv", "r", encoding="cp1251") as file:
            reader = csv.DictReader(file, delimiter=",")
            for line in reader:
                date_list.append(line['date'])

        if date_list[-1] != current_date:
            data = {'date': current_date,
                    'old_price': OLD_PRICE,
                    'new_price': new_price,
                    'percentage': price_diff_as_percent}
            with open("gold.csv", "a", encoding="cp1251", newline="") as f:
                fieldnames = ["date", "old_price", "new_price", "percentage"]
                writer = csv.DictWriter(f, fieldnames, delimiter=",")
                writer.writerow(data)


    def show_price_change_graph():
        dataframe = pd.read_csv('gold.csv', sep=',')
        dataframe.drop_duplicates('date')
        plt.plot(dataframe['date'], dataframe['old_price'])
        plt.plot(dataframe['date'], dataframe['new_price'])

        # Give names to the plot and its axis
        plt.title('10-gram gold bar price fluctuation graph')
        plt.xlabel('Dates')
        plt.ylabel('Price [in roubles]')

        # Make dates inscriptions inclined for readability
        plt.xticks(dataframe['date'], rotation='25')
        plt.show()


    OLD_PRICE = 31341
    new_price = get_gold_bar_price_from_xls(xls_file_name)
    price_diff_as_percent = int(((new_price - OLD_PRICE) * 100) / OLD_PRICE)
    print(textwrap.dedent(f"""
        {new_price} - 31341 = 
        {int(new_price - OLD_PRICE)} rub., 
        {price_diff_as_percent}%
        """).replace("\n", ""))

    save_new_price_to_make_a_graph()
    show_price_change_graph()

if __name__ == "__main__":
    main()
