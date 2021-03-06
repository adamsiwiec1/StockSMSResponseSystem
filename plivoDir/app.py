import plivo
from flask import Flask, request, make_response, Response
from plivo import plivoxml
from dictionary import StockDictionary
from plivoDir import messages
from stock import Stock
from yfin import StockScraper
import yfin

# Stock List
stockObjects = []

# Flask dev server object
app = Flask(__name__)

# Web Scraper Object - used for 'self' in methods.
stockScraper = StockScraper()


def print_stocks():
    string = ""
    for stock in stockObjects:
        string += str(stock.ticker.upper() + "\n")
    if len(string) < 4:
        string = "You have not added any stocks. Text /add to append."
    return string


def stock_price(ack):
    ack.lower()
    if ack == "ERROR":
        string = "Error"
    elif ack != "ERROR":
        for stock in stockObjects:
            stocks = [f"{stock.ticker.upper()} {stock.price}"
                      f"\nFloor:   {stock.floor}"
                      f"\nCeiling: {stock.ceiling}"]
            for stock in range(len(stocks)):
                if ack.upper() in stocks[stock]:
                    return stocks[stock]
    else:
        return "You broke the matrix. Try again."


def get_input(detail):
    details = detail.split(' ', 2)
    return details[1]


def check_for_none(stocks):

    for stock in stocks:
        if stock.acronym is None:
            del stock

    return stocks


# Text reply system
@app.route('/sms', methods=['POST'])
def inbound_sms():
    from_number = request.values.get('From')
    to_number = request.values.get('To')
    response = request.values.get('Text')
    response = response.lower()
    print('%s said %s' % (from_number, response))
    print(stockObjects)
    stockAck = ""
    stockFloor = ""
    stockCeiling = ""

    # Handle new incoming stock
    if "-" in str(response):
        newStock = str(response).rsplit("-", 3)
        stockAck = newStock[0]
        stockFloor = newStock[1]
        stockCeiling = newStock[2]

    resp = plivoxml.ResponseElement()  # Response object for Plivo

    # Help Menu
    if "menu" in response:
        resp.add(plivoxml.MessageElement("StockScraper Commands:\n/start\n/stop\n/price STOK\n/mystocks\n/details STOK\n/add\n/remove", src=to_number, dst=from_number))

    # Gets a price of any NASDAQ or COLE stock, even ones not in /mystocks
    elif '/price' in response:
        ack = get_input(response)
        messages.send_price(ack, from_number)

    # Start Looking for Alerts
    elif response == "/start":
        stockCount = len(stockObjects)
        if stockCount > 0:
            messages.started_scraper_message(from_number)
            stocks = stockObjects
            StockScraper.start_scraper(stockScraper, stocks, from_number)
            return Response(resp.to_string(), mimetype='application/xml')
        else:
            resp.add(plivoxml.MessageElement("You must add stocks before starting the scraper. Reply with /add.", src=to_number, dst=from_number))

    # Stop Looking for Alerts
    elif response == "/stop":
        StockScraper.stop_scraper(stockScraper)
        resp.add(plivoxml.MessageElement("StockScraper has ended. Reply '/start' to begin.", src=to_number, dst=from_number))

    # Reply with acronyms of all stocks the user has added
    elif response == "/mystocks":
        resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))

    # Reply with details of a stock
    elif "/details" in response:
        ack = get_input(response)
        messages.send_details(ack, from_number)

    # Reply with directions on how to add a stock
    elif "/add" in response:
        resp.add(plivoxml.MessageElement("Please reply with the stock acronym you would like to add followed by its floor/ceiling.\n\nEx: NOK-1.00-4.50", src=to_number, dst=from_number))

    # Remove a stock (or multiple) from /mystocks
    elif "/remove" in response:
        if len(response) > 7:
            for stock in stockObjects:
                if stock.ticker not in response:
                    response = response.split(" ", 2)
                    messages.remove_stock_notfound(response[1], from_number)
                elif stock.acronym in response:
                    ack = stock.acronym
                    del stock
                    if len(ack) != 0:
                        messages.remove_stock(ack, from_number)
                else:
                    messages.broke_matrix(from_number)
            resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
        else:
            resp.add(plivoxml.MessageElement(f"Please reply with the stock you would like to remove from /mystocks.\n\n Ex: /remove NOK", src=to_number, dst=from_number))

    # Add a stock to /mystocks
    elif stockAck in StockDictionary.NASDAQ or StockDictionary.COLE and stockFloor and stockCeiling:
        try:
            float(stockFloor)
            float(stockCeiling)
            stockObjects.append(Stock(f"{stockAck.upper()}", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, stockFloor, stockCeiling))
            resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
        except ValueError or Exception as e:
            print(str(e))
            resp.add(plivoxml.MessageElement("You failed to enter a stock correctly. Type /add to try again.", src=to_number, dst=from_number))

    # Exceptions
    elif stockAck and not stockFloor or stockCeiling:
        resp.add(plivoxml.MessageElement("You failed to enter a stock correctly. Type /add to try again.", src=to_number, dst=from_number))
    else:
        resp.add(plivoxml.MessageElement("Unrecognized command. Please type 'menu' for help.", src=to_number, dst=from_number))

    # Print details in console
    print(resp.to_string())
    print(stockObjects)

    # Return the response that was chosen by the above selection structure to the user
    return Response(resp.to_string(), mimetype='application/xml')


if __name__ == '__main__':
    app.run()
