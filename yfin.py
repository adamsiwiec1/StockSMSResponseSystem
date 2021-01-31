# Using yahoo finance api
import plivo
import yfinance as yf
from termcolor import colored
from stock import Stock


class StockScraper:
    def __init__(self):
        self.stop = False

    def alert_message(self, stock, to_number):
        client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
        message_created = client.messages.create(
            src='+15709985164',
            dst=f'{to_number}',
            text=f'ALERT: {stock.acronym} at {stock.float_price}'
        )

    def limit_message(self, stock, to_number):
        client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
        message_created = client.messages.create(
            src='+15709985164',
            dst=f'{to_number}',
            text=f'LIMIT REACHED - you will stop receiving alerts for this stock. ALERT: {stock.acronym} at {stock.float_price}'
        )

    def start_scraper(self, stocks, to_number):
        self.stop = False
        while not self.stop:
            stockDictList = create_infoDict_list(stocks)
            for stock in stockDictList:
                sendAlert = compare_price(stock.price, stock.floor, stock.ceiling)
                if sendAlert and stock.count < 3:
                    stock.alert_count()
                    self.alert_message(stock, to_number)
                if sendAlert and stock.count >= 3 and stock.limitCount < 1:
                    stock.limit_count()
                    self.limit_message(stock, to_number)

    def stop_scraper(self):
        self.stop = True

# Mock Stocks
stocksList = [Stock(str('NOK'), "", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 6.00)]
stocksList.append(Stock(str('AZN'), "", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 45.00, 50.00))
stocksList.append(Stock(str('AAPL'), "", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 99.00, 500.00))
stocksList.append(Stock(str('TSLA'), "", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 500.00, 900.00))


def compare_price(stock_price, low, high):
    current_price = float(stock_price)

    if current_price < 0:
        print(colored("Error comparing stocks price.", "red"))
        return False
    elif current_price <= float(low):
        return True
    elif current_price >= float(high):
        return True
    else:
        return False

def create_infoDict_list(stocks):
    dictList = []
    for stock in stocks:
        if stock.volume is not None:
            stokDict = get_info(str(stock.ticker))
        try:
            stock.ticker = stokDict["Ticker"]
            stock.name = stokDict["Name"]
            stock.price = stokDict["Price"]
            stock.ask = stokDict["Ask"]
            stock.bid = stokDict["Bid"]
            stock.daylow = stokDict["DayLow"]
            stock.dayhigh = stokDict["DayHigh"]
            stock.volume = stokDict["Volume"]
            stock.marketOpen = stokDict["MarketOpen"]
            stock.marketClose = 'MarketClose'
            dictList.append(stock.__dict__)
        except UnboundLocalError as e:
            print("Error" + str(e))

    return dictList


def get_info(ticker):
    stock = yf.Ticker(ticker)

    infoDict = {

        # current
        "Ticker": stock.info['symbol'],
        "Name": stock.info['longName'],
        "Price": stock.info['regularMarketPrice'],
        "Ask": stock.info['ask'],
        "Bid": stock.info['bid'],
        "DayLow": stock.info['dayLow'],
        "DayHigh": stock.info['dayHigh'],
        "Volume": stock.info['regularMarketVolume'],
        "MarketOpen": stock.info['regularMarketOpen'],
        "MarketClose": stock.info['regularMarketPreviousClose'],

        # details
        "52WeekLow": stock.info['fiftyTwoWeekLow'],
        "52WeekHigh": stock.info['fiftyTwoWeekHigh'],
        "50DayAvg": stock.info['fiftyDayAverage'],
        "200DayAvg": stock.info['twoHundredDayAverage'],
        "AvgVolume": stock.info['averageVolume'],
        "10DayAvgVolume": stock.info['averageDailyVolume10Day'],

        # extra details
        "Sector": stock.info['sector'],
        "BookValue": stock.info['bookValue'],
        "YtdReturn": stock.info['ytdReturn'],
        "LastDividendValue": stock.info['lastDividendValue'],
        "ShareShort": stock.info['sharesShort'],
        "FloatShares": stock.info['floatShares'],
        "Employees": stock.info['fullTimeEmployees']


    }

    return infoDict


def get_stock_price(ack):
    stock = yf.Ticker(ack)
    price = stock.info["regularMarketPrice"]
    return f"{ack} {price}"


def get_stock_details(ack):
    stock = yf.Ticker(ack)
    ticker = stock.info['symbol']
    name = stock.info['longName']
    price = stock.info['regularMarketPrice']
    ask = stock.info['ask']
    bid = stock.info['bid']
    dayLow = stock.info['dayLow']
    dayHigh = stock.info['dayHigh']
    volume = stock.info['regularMarketVolume']
    marketOpen = stock.info['regularMarketOpen']
    marketClose = stock.info['regularMarketPreviousClose']

    return f"{ticker}\n{name}\nPrice: {price}\nAsk: {ask}\nBid: {bid}\nMrktOpen: {marketOpen}\nDayHigh: {dayHigh}" \
           f"\nDayLow: {dayLow}\nVolume: {volume}\nOnPrevClose: {marketClose}"
