from stock.driver import arg_parser, Ticker, fetcher, Query, main
import stock.driver as driver
import pytest
import sqlite3
import os

@pytest.fixture
def db():
    conn = sqlite3.connect("stocks_new.db")
    return conn

@pytest.fixture
def fetch():
    t = "60"
    db = "stock.db"
    return fetcher(t, db)

@pytest.fixture
def fetch1():
    t = "60"
    db = "stock.db"
    return fetcher(t, db)

@pytest.fixture
def args():
    return ["5", "300", "stocks_new.db"]

def test_main():
    m = main(["driver.py", "1=Ticker", "1=5", "2=300", "3=stocks_new.db"])

def test_arg_parser():
    l = ["o=0","a=1","b=2","c=3"]
    arg_list = ["1","2","3"]
    assert arg_parser(l) == arg_list

def test_fetcher_params(fetch):
    f = fetch

def test_update_stock(db, fetch):
    tic = "AAPL"
    c = db.cursor()
    c.execute("create table if not exists StockData(Time text, Symbol text, Low text, High text, Open text, Close text, Price text, Volume text)")
    f = fetch.update_stock(tic,c)

def test_fetch_all_data_120(fetch, args):
    # time_limit is 120 seconds
    fname = os.path.join(os.path.dirname(__file__), 'tickers.txt')
    f = fetch.fetch_all_data(args, fname)

def test_fetch_all_data_60(fetch1, args):
    # time_limit is 60 seconds
    fname = os.path.join(os.path.dirname(__file__), 'tickers.txt')
    f = fetch1.fetch_all_data(args, fname)

def test_main_fetcher():
    main(['driver.py', '1=Ticker', '1=5', '2=60', '3=stocks_new.db'])
    main(['driver.py', '2=Fetcher', '1=5', '2=60', '3=stocks_new.db'])
    main(['driver.py', '3=Query', '1=5', '2=300', '3=stocks_new.db'])
    main(['driver.py', '4=Stocks', '1=5', '2=300', '3=stocks_new.db'])

def test_ticker_max():
    """
    args:
        none
    use:
        verify that save_tickers fetches no more then 110 tickers
    """
    myTicker = Ticker()
    myTicker.ticker_file_name = "tickers_test.txt"
    myTicker.save_tickers(111)
    f = open(myTicker.ticker_file_name)
    counter = 0
    for line in f.readlines():
        counter += 1
    assert counter == 110

def test_ticker_count():
    """
    args:
        none
    use:
        verify that save_tickers fetches the number of symbols specified.
    """
    myTicker = Ticker()
    myTicker.ticker_file_name = "tickers_test.txt"
    myTicker.save_tickers(2)
    f = open(myTicker.ticker_file_name)
    counter = 0
    for line in f.readlines():
        counter += 1
    assert counter == 2