import csv
from datetime import date
import json
import matplotlib.pyplot as plt
import pandas as pd
import requests
import xlrd


def main():
    def get_current_date_as_string():
        current_date = date.today()
        date_as_string = current_date.strftime('%d.%m.%Y')
        return date_as_string


    def get_current_month():
        current_month = int(date_as_string[3:5])
        return current_month


    def get_current_year():
        current_year = int(date_as_string[6:10])
        return current_year


    date_as_string = get_current_date_as_string()
    month = get_current_month()
    year = get_current_year()


    def compile_bank_url(month, year):
        url_beginning = "https://www.sberbank.ru/proxy/services/dict-services/document/list?groupCode=279&regionCode=77&month="
        url = url_beginning + str(month) + '&year=' + str(year)
        return url


    def get_bank_url_contents(url):
        try:
            result = requests.get(url)
            #result.raise_for_status()
            return result.content
        except(requests.RequestException, ValueError):
            print("Network error")
            return False


    url = compile_bank_url(month, year)
    url_contents = get_bank_url_contents(url)

    reasonable_amount_of_elements_per_page_in_action = 3
    if len(url_contents) < reasonable_amount_of_elements_per_page_in_action:
        while month > 0:
            month -= 1
            url = compile_bank_url(month, year)
            url_contents = get_bank_url_contents(url)
            if len(url_contents) > reasonable_amount_of_elements_per_page_in_action:
                break


    def download_file_with_gold_bar_prices(url_contents):
        if url_contents:
            most_recent_file_available = json.loads(url_contents)[-1]
            part_of_url_of_most_recent_file = most_recent_file_available['fileUrl']
            prices_file_url = "http://sberbank.ru" + part_of_url_of_most_recent_file
            file_with_prices = requests.get(prices_file_url, allow_redirects=True)
            open('gold.xls', 'wb').write(file_with_prices.content)
        else:
            print("File with gold_bar prices was not found")


    download_file_with_gold_bar_prices(url_contents)


    def retrieve_gold_bar_new_price():
        book = xlrd.open_workbook("gold.xls", encoding_override="cp1252")
        sheet = book.sheet_by_index(0)
        new_price = int(sheet.cell_value(11, 3))
        return new_price


    new_price = retrieve_gold_bar_new_price()
    OLD_PRICE = 31341


    def print_price_comparison():
        price_difference = new_price - OLD_PRICE
        price_difference_as_percent = int((price_difference * 100) / OLD_PRICE)
        print(f"{new_price} - 31341 = {int(price_difference)} rub., {price_difference_as_percent}%")
        return price_difference_as_percent


    price_difference_as_percent = print_price_comparison()


    def save_new_price_to_make_a_graph():
        date_list = []
        with open("gold.csv", "r", encoding="cp1251") as file:
            reader = csv.DictReader(file, delimiter=",")
            for line in reader:
                date_list.append(line['date'])

        if date_list[-1] != date_as_string:
            data = {'date': date_as_string, 'old_price': OLD_PRICE, 'new_price': new_price,
                   'percentage': price_difference_as_percent}
            with open("gold.csv", "a", encoding="cp1251", newline="") as f:
                fieldnames = ["date", "old_price", "new_price", "percentage"]
                writer = csv.DictWriter(f, fieldnames, delimiter=",")
                writer.writerow(data)


    save_new_price_to_make_a_graph()


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

    show_price_change_graph()

if __name__ == "__main__":
    main()
