# Using yahoo finance api
import plivo
import yfinance as yf


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

    print(infoDict)

get_info("azn")