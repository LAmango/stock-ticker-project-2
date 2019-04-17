####################
### Ticker Class ###
####################

# [] – Have a function, say save tickers that fetches the first 
#      n valid tickers from the URL 1 and writes the tickers in 
#      a file, say tickers.txt.
# [] – To ensure that a ticker is valid, you should use the 
#      iex-api-python to verify that the price function for 
#      the Stock corresponding to the fetched ticker works. 
#      That is, if there are some tickers for which the price() 
#      function of the iex API does not work, then that ticker 
#      should not be written to the file.
# [] – Write one ticker symbol per line of the file tickers.txt. 
#      The number n will be provided to the driver
#      as an optional argument and will be at most 110.
# [] – The class must have a method for initialization of its 
#      objects and any other methods you feel are necessary.

#####################
### Fetcher Class ###
#####################

# [x] – Read all the tickers from an input file (tickers.txt) or use some function of the Tickers class to fetch
# the tickers.
# [x] – Define a function that updates the current stock information for the ticker that is passed as an argument. 
#   The information is updated in an information database (say stocks now.db for example). The name of the table will be StockData. 
#   Use sqlite3 database.
# [x] – There should be another function, say fetch all data() of the class that calls the above function for each input ticker.
# [x] – The fetch all data() function should run for specified time period, say time lim in seconds and update the data in the database table.
# [x] – For each ticker in the tickers.txt file, the database table, should have one row for each minute.
# [x] – The Time column should contain time in the HH:MM format with HH ranging from 00 to 23. There
#   should be one and only one row corresponding to a specific value of Time and Ticker.
# [x] – In order to extract the stock information for a ticker, say ”AAPL”, you should use the iex-api-python
#   which is described here: https://pypi.org/project/iex-api-python/. You need to fetch the current data for the following fields: low, high, open, close, latestPrice, latestVolume. Use the
#   quote() function of the Stock corresponding to the ticker.
# [x] – The table must have following columns:
#   Time, Ticker, Low, High, Open, Close, Price, Volume
# [x] – Store the time of the query and the respective keys and values in the database table where the Price
#   column stores latestPrice and Volume column stores latestVolume. For each iteration, during which
#   you save the data for a specific minute, you may wait till the start of the next minute, say, 12:37 and
#   then save the data for all tickers during that iteration with the Time field set to the minute (12:37).
# [x] – The class must have a method for initialization of its objects and any other methods you feel are
#   necessary.
# [x] – You may assume that your code will be tested on an empty database that you have to create based on
#   the name of the database file provided.
# [x] – Please use the information on the API page to figure out how to install iex-api-python. The page also
#   has the information for fetching necessary data about a stock ticker.

###################
### Query Class ###
###################

# [] – Define a function that prints and/or returns the details corresponding to a specific time and ticker
#   symbol to the terminal.
# [] – The class must have a method for initialization of its objects and any other methods you feel are
#   necessary.

import sys
import requests
import re
from datetime import datetime, time
import json
import csv
import pandas as pd
import asyncio
from iex import Stock
import time
import sqlite3
from itertools import islice

class Ticker():
    # initialize objects that are needed
    def __init__(self):
        self.myList = []
        self.counter = 0
        self.ticker_file_name = "tickers.txt"

    

    # function to write 1 ticker per line from URL, save to tickers.txt

    def save_tickers(self, n):
        # max 110 tickers to file
        for x in range(1,5):
            content=requests.get("https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&page=" + str(x))
            # REGEX to find stock symbol from page.
            self.myList += re.findall(r'<a href="https://www.nasdaq.com/symbol/[^"/]+">\s+([A-Z]+)</a>',str(content.text))
        # check if ticker is valid using price()
        fp = open(self.ticker_file_name, "w")

        # Checks to see if the price for the ticker is available.
        def is_valid(symbol):
            try:
                Stock(symbol).price()
                return True
            except:
                return False
                
        for i in self.myList:
            if is_valid(i):
                fp.write(i + "\n")
                counter += 1
                if counter > n:
                    break
                if counter == n:
                    break
        fp.close()



class fetcher():
    def __init__(self, time_limit, db):
        """
        Fetcher Class
            
        args:
            time_limit: the amount of time to run the fetch_all_data method for.
            db: name of the database given from a command line arg

        use:
            initialized the time_limit and database name of the class
        """
        self.__db = db
        self.__time_limit = int(time_limit)
        

    def update_stock(self, ticker, c):
        """
        args:
            ticker: the ticker to update
            c: cursor to execute sql commands
        use:
            request info of the ticker and update the database with the info
        """
        t = datetime.time(datetime.now()).isoformat(timespec='minutes')
        q = Stock(ticker).quote()
        stock = [t, q['symbol'], q['low'], q['high'], q['open'], q['close'], q['latestPrice'], q['latestVolume']]
        
        insert = "insert into StockData values (?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(insert, stock)

        print(stock)

    def fetch_all_data(self, args, filename):
        """
        use:
            calls the update_stock method for each ticker in self.tickers.
            should run for a specific time period
        """
        # get the number of tickers requested
        with open(filename) as tickers:
            tickers = [line.split("\n")[0] for line in islice(tickers, int(args[0]))]

        # start and create database
        db = sqlite3.connect(self.__db)
        c = db.cursor()
        drop_table = "drop table if exists StockData"
        create_table = "create table StockData(Time text, Symbol text, Low text, High text, Open text, Close text, Price text, Volume text)"
        c.execute(drop_table)
        c.execute(create_table)

        start_time = time.time()
        t = 1

        # run update_stock method on each ticker provided every minute untill time_limit is reached
        while (time.time() - start_time) < self.__time_limit:
            for tic in tickers:
                self.update_stock(tic, c)
            print(f'minute {t}')

            if (time.time() - start_time) + 60 > self.__time_limit:
                break
            else:
                time.sleep(60)

            t += 1

        header = f"{'Time':<10}{'Symbol':<10}{'Price':<10}{'Volume':<10}"
        print(header)

        sql_cmd = "select * from StockData"
        for t, s, *h, p, v in c.execute(sql_cmd):
            print(f"{t:<10}{s:<10}{p:<10}{v:<10}")

        # commit and close database
        db.commit()
        db.close()

def main(args):
    
    fname = "stock/tickers.txt"

    operation, *args = arg_parser(args)

    if operation == "Ticker":
        myTicker = Ticker()
        print(args)
        myTicker.save_tickers(args[0])    
        pass
    elif operation == "Fetcher":
        f = fetcher(args[1], args[2])
        
        f.fetch_all_data(args, fname)
    elif operation == "Query":
        pass
    else:
        print("Invalid use of '--operation'")


def arg_parser(args):
    """
    args:
        args: sys.argv list
    use:
        parses the list and splits them to get rid of the command line flag names
    """
    return [x.split("=")[1] for x in args[1:]]


if __name__ == '__main__':
    main(sys.argv)
