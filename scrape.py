import plivo
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Test change
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
            stockList = scrape(stocks)
            for stock in stocks:
                sendAlert = compare_price(stock.float_price, stock.floor, stock.ceiling)
                if sendAlert and stock.count < 3:
                    stock.alert_count()
                    self.alert_message(stock, to_number)
                if sendAlert and stock.count >= 3 and stock.limitCount < 1:
                    stock.limit_count()
                    self.limit_message(stock, to_number)

    def stop_scraper(self):
        self.stop = True


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


def pull_stock_info(stock):
    print("Pulling info for " + stock.acronym)

    # Send HTTP request
    try:
        yahoo = f"https://finance.yahoo.com/quote/{stock.acronym}?p={stock.acronym}&.tsrc=fin-srch"
        page = requests.get(yahoo)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
            return data
        except AttributeError as e:
            print(stock)
            print(e)
    except requests.ConnectionError as e:
        print("Connection Error:" + str(e))
    except requests.Timeout as e:
        print("Timeout Error" + str(e))
    except requests.RequestException as e:
        print("General Error:" + str(e))
    except KeyboardInterrupt:
        print("Exiting the program.")


def get_price(stock_info):
    # Need to add exception handling in this method, there is already some later in in scrape()***********
    plus = '+'
    minus = '-'
    period = "."

    # Account for different format when market is closed or open

    if 'close' in stock_info:
            info_array = stock_info.rsplit(' ', 5)
    if 'open' in stock_info:
            info_array = stock_info.rsplit(' ', 8)

    # Account for different format when stocks is up/down
    if plus in info_array[0]:  # UnboundLocalError needs to be accounted
        price = info_array[0].split('+')[0]
    elif minus in info_array[0]:
        price = info_array[0].split('-')[0]
    else:
        count = 0
        for period in info_array[0]:
            if period == '.':
                count = count + 1
                if count >= 2:
                    price = info_array[0].split('.', 2)[0] + info_array[0].split('.')[1]
            else:
                print("Error")
                return "0.00"
    if price is not None:
        return price
    else:
        print("Error")
        return "0.00"


def scrape(stocks):  # Needs Cleaned - move outside exceptions into method?
    count = len(stocks)
    raw_stock = []
    price_stock = []
    for num in range(count):
        if stocks[num] is not None:
            raw_stock.append(pull_stock_info(stocks[num]))
    for num in range(count):
        price = get_price(raw_stock[num])
        if float(price) <= 0:
            print(colored("There was an error retrieving a stocks price.", "red"))
            price_stock.append(price)
        else:
            price_stock.append(price)

    for num in range(count):
        stocks[num].raw = raw_stock[num]
        stocks[num].price = price_stock[num]
        try:
            if "," in price_stock[num]:
                price_stock[num] = price_stock[num].replace(',', '')
            elif price_stock[num]:
                stocks[num].float_price = float(price_stock[num])
            else:
                raise ValueError("|----$$Price Conversion Failure$$----|")
        except ValueError as e:
            print(f"Failed to pull {stocks[num].name} ----| Value Error: {e}")
    return stocks


def scrape_price(ack):
    yahoo = f"https://finance.yahoo.com/quote/{ack}?p={ack}&.tsrc=fin-srch"
    page = requests.get(yahoo)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
    except AttributeError:
        return "Enter a valid stock."
    price = get_price(data)
    return f"{ack} {price}"

