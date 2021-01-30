import requests
from bs4 import BeautifulSoup
from termcolor import colored


class StockScraper(object):

    def __init__(self):
        self.stop = False

    @classmethod
    def stop_scraper(cls):
        stop = True

    def pull_stock_info(self, stock):
        print("Pulling info for " + stock.acronym)

        # Send HTTP request
        try:
            yahoo = f"https://finance.yahoo.com/quote/{stock.acronym}?p={stock.acronym}&.tsrc=fin-srch"
            page = requests.get(yahoo)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:  # Scrape html from the webpage
                count = 0
                data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
                if data is None:
                    while count < 4:
                        count += 1
                        print(colored(f"!!!!Failed to pull {stock.acronym} - Trying again!!!!\n"), "red")
                        data = soup.find(class_="My(6px) Pos(r) smartphone_Mt(6px)").text
                        if data is not None:
                            count = 4
                return data
            except AttributeError or UnboundLocalError:
                print(colored(f"\n|----!!!!FAILED TO PULL DATA FOR {stock.acronym} !!!!----|\n", "red"))
                print(colored("Restarting the program...", "red"))
        except requests.ConnectionError as e:
            print("Connection Error:" + str(e))
        except requests.Timeout as e:
            print("Timeout Error" + str(e))
        except requests.RequestException as e:
            print("General Error:" + str(e))
        except KeyboardInterrupt:
            print("Exiting the program.")

    def get_price(self, stock_info):
        # Need to add exception handling in this method, there is already some later in in scrape()***********
        plus = '+'
        minus = '-'
        period = "."

        # Account for different format when market is closed or open
        if 'close' in stock_info:
            info_array = stock_info.rsplit(' ', 5)
        if 'open' in stock_info:
            info_array = stock_info.rsplit(' ', 8)
        # elif 'open' or 'close' not in stock_info:
        #     print(colored("Error: Not open or closed?", "red"))
        #     return "0.00"

        # Account for different format when stocks is up/down
        if plus in info_array[0]:
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
        return price

    def scrape(self, stocks):  # Needs Cleaned - move outside exceptions into method?
        count = len(stocks)
        raw_stock = []
        price_stock = []
        for num in range(count):
            raw_stock.append(self.pull_stock_info(stocks[num]))

        for num in range(count):
            price = self.get_price(raw_stock[num])
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


    def start_scraper(self, stocks):
        while not StockScraper().stop:
            self.scrape(stocks)
