import csv
from datetime import date
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import textwrap
import xlrd
from typing import Union


def get_cur_date() -> str:
    cur_date = date.today() # 07.11.2020
    return cur_date.strftime('%d.%m.%Y')


def get_cur_month(cur_date: str) -> int:
    return int(cur_date[3:5]) - 1 # months start from 0


def get_cur_year(cur_date: str) -> int:
    return int(cur_date[6:10])


def compile_bank_url(cur_month: int, cur_year: int) -> str:
    url_start = "https://www.sberbank.ru/proxy/services/dict-services/"\
                "document/list?groupCode=279&regionCode=77&month="
    return url_start + str(cur_month) + '&year=' + str(cur_year)


def get_bank_url_content(cur_month: int, cur_year: int) -> bytes:
    url = compile_bank_url(cur_month, cur_year)
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
    book = xlrd.open_workbook(xls_file_name)
    sheet = book.sheet_by_index(0)
    return int(sheet.cell_value(11, 3))


def main():
    cur_date = get_cur_date()
    cur_month = get_cur_month(cur_date)
    cur_year = get_cur_year(cur_date)
    url_content = get_bank_url_content(cur_month, cur_year)

    min_content_size = 3 # '[]' for empty response
    min_year_to_check = 2018
    while len(url_content) < min_content_size and \
        cur_year >= min_year_to_check:
        # check previous months if bank has no prices for current month
        if cur_month > 0:
            cur_month -= 1
        elif cur_month == 0:
            cur_month = 11
            cur_year -= 1
        url_content = get_bank_url_content(cur_month, cur_year)

    xls_file_name = 'gold.xls'
    if url_content:
        file_content = download_file_with_prices(url_content)
        with open(xls_file_name, 'wb') as out:
            out.write(file_content)
    else:
        print("File with gold bar prices was not found")
    

    def save_new_price_to_make_a_graph():
        date_list: list = []
        with open("gold.csv", "r") as file:
            reader = csv.DictReader(file, delimiter=",")
            for line in reader:
                date_list.append(line['date'])

        if date_list[-1] != cur_date:
            data = {'date': cur_date,
                    'old_price': OLD_PRICE,
                    'new_price': new_price,
                    'percentage': price_diff_as_percent}
            with open("gold.csv", "a", newline="") as f:
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
