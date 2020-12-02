import gold
import pytest
import tempfile
import xlrd


def test_current_date():
    date = gold.get_current_date()
    assert type(date) == str, "Current date is not a string"
    assert len(date) == len("DD.MM.YYYY"), "Current date has a wrong length"


def test_current_month():
    month = gold.get_current_month("07.11.2020")
    assert type(month) == int, "Current month is not an integer"
    assert 0 <= month <= 11, "Current month has an unreal number"


def test_current_year():
    year = gold.get_current_year("07.11.2020")
    assert type(year) == int, "Current year is not an integer"
    assert len(str(year)) == 4, "Current year is too short to be true"


def test_bank_url():
    month = 1
    year = 2021
    bank_url = gold.compile_bank_url(month, year)
    assert type(bank_url) == str, "Bank url is not a string"
    assert len(bank_url) > 110, "Bank url is too short"
    assert "sberbank" in bank_url, "Bank url content is wrong"
    

def test_check_web_page_is_available():
    month = 1
    year = 2021
    request_result = gold.get_bank_url_content(month, year)
    assert request_result is not False, "Request is not successful"
    assert type(request_result) == bytes, "Type of requst result isn't bytes"


def test_check_xls_file_is_downloaded():
    month = 1
    year = 2021
    url_content = gold.get_bank_url_content(month, year)
    min_content_size = 3 # '[]' for empty response
    min_year_to_check = 2018
    while len(url_content) < min_content_size and year >= min_year_to_check:
        # check previous months if bank has no prices for current month
        if month > 0:
            month -= 1
        elif month == 0:
            month = 11
            year -= 1
        url_content = gold.get_bank_url_content(month, year)
    file_content = gold.download_file_with_prices(url_content)
    assert file_content is not False, "File was not downloaded"


def test_received_price():
    month = 12
    year = 2020
    url_content = gold.get_bank_url_content(month, year)
    min_content_size = 3 # '[]' for empty response
    min_year_to_check = 2018
    while len(url_content) < min_content_size and year >= min_year_to_check:
        # check previous months if bank has no prices for current month
        if month > 0:
            month -= 1
        elif month == 0:
            month = 11
            year -= 1
        url_content = gold.get_bank_url_content(month, year)

    file_content = gold.download_file_with_prices(url_content)
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(file_content)
        gold_bar_price = gold.get_gold_bar_price_from_xls(temp.name)
        assert type(gold_bar_price) == int, "Gold bar price is not an integer"
        assert gold_bar_price > 0, "Gold bar price is negative"

        book = xlrd.open_workbook(temp.name, encoding_override="cp1252")
        sheet = book.sheet_by_index(0)
        bar_metal = sheet.cell_value(8, 0)
        assert bar_metal.strip() == "Золото", "Price is not for a bar of gold"
        bar_weight = sheet.cell_value(11, 0) # I'm interested in 10-gram bar
        assert int(bar_weight) == 10, "The price weight is wrong"

        temp.flush()
