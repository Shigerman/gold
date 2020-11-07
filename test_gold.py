import pytest
import gold


def test_current_date():
    date = gold.get_current_date()
    assert type(date) == str, "Current date is not a string"
    assert len(date) == 10, "Current date has a wrong length"


def test_current_month():
    month = gold.get_current_month("07.11.2020")
    assert type(month) == int, "Current month is not an integer"
    assert 0 <= month <= 11, "Current month has an unreal number"


def test_current_year():
    year = gold.get_current_year("07.11.2020")
    assert type(year) == int, "Current year is not an integer"
    assert len(str(year)) == 4, "Current year is too short to be true"


def test_bank_url():
    bank_url = gold.compile_bank_url(5, 2020)
    assert type(bank_url) == str, "Bank url is not a string"
    assert len(bank_url) > 110, "Bank url is too short"
    assert "sberbank" in bank_url, "Bank url content is wrong"


test_current_date()
test_current_month()
test_current_year()
test_bank_url()
