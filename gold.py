import csv
from datetime import date
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import textwrap
import xlrd


def get_current_date():
    current_date = date.today() # 07.11.2020
    return current_date.strftime('%d.%m.%Y')


def get_current_month(current_date: str):
    return int(current_date[3:5]) - 1 # months start from 0


def get_current_year(current_date: str):
    return int(current_date[6:10])


def compile_bank_url(current_month, current_year):
    url_start = "https://www.sberbank.ru/proxy/services/dict-services/"\
                "document/list?groupCode=279&regionCode=77&month="
    return url_start + str(current_month) + '&year=' + str(current_year)


def request_price_files(current_month, current_year):
    url = compile_bank_url(current_month, current_year)
    try:
        result = requests.get(url)
        return result.content
    except(requests.RequestException, ValueError):
        print("Network error")
        return False


def download_gold_bar_prices(price_files):
    most_recent_file_available = json.loads(price_files)[-1]
    url_part_of_most_recent_file = most_recent_file_available['fileUrl']
    prices_file_url = 'http://sberbank.ru' + url_part_of_most_recent_file
    file_with_prices = requests.get(prices_file_url, allow_redirects=True)
    return file_with_prices.content


def gold_bar_price_from_xls(xls_file_name):
    book = xlrd.open_workbook(xls_file_name, encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    return int(sheet.cell_value(11, 3))


def main():
    current_date = get_current_date()
    current_month = get_current_month(current_date)
    current_year = get_current_year(current_date)
    price_files = request_price_files(current_month, current_year)

    min_contents_size = 3 # '[]' for empty response
    if len(price_files) < min_contents_size:
        while current_month > 0:
            current_month -= 1
            price_files = request_price_files(current_month, current_year)
            if len(price_files) > min_contents_size:
                break

    if price_files:
        file_content = download_gold_bar_prices(price_files)
        xls_file_name = 'gold.xls'
        open(xls_file_name, 'wb').write(file_content)
    else:
        print("File with gold bar prices was not found")
    

    def save_new_price_to_make_a_graph():
        date_list = []
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
    xls_file_name = 'gold.xls'
    new_price = gold_bar_price_from_xls(xls_file_name)
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
