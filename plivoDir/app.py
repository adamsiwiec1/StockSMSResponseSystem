from flask import Flask, request, make_response, Response
from plivo import plivoxml
from dictionary import StockDictionary
from stock import Stock
from scrape import StockScraper

# Stock List
stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0)]
app = Flask(__name__)

stockScraper = StockScraper()

def print_stocks():
    string = ""
    for stock in stockObjects:
        string += str(stock.acronym.upper() + f" {stock.price}\n")
    if len(string) < 4:
        string = "You have not added any stocks. Text /add to append."
    return string


def stock_price(ack):
    ack.lower()
    if ack == "ERROR":
        string = "Error"
    elif ack != "ERROR":
        for stock in stockObjects:
            stocks = [f"{stock.acronym.upper()} {stock.float_price}"
                      f"\nFloor:   {stock.floor}"
                      f"\nCeiling: {stock.ceiling}"]
            for stock in range(len(stocks)):
                if ack.upper() in stocks[stock]:
                    return stocks[stock]
    else:
        return "You broke the matrix. Try again."


def get_stock_user(detail):
    details = detail.split(' ', 2)
    return details[1]


# Text reply system
@app.route('/sms', methods=['POST'])
def inbound_sms():
    from_number = request.values.get('From')
    to_number = request.values.get('To')
    response = request.values.get('Text')
    response = response.lower()
    print('%s said %s' % (from_number, response))

    stockAck = ""
    stockFloor = ""
    stockCeiling = ""

    # Handle new incoming stock
    if "-" in str(response):
        newStock = str(response).rsplit("-", 3)
        stockAck = newStock[0]
        stockFloor = newStock[1]
        stockCeiling = newStock[2]

    resp = plivoxml.ResponseElement()
    make_response("RESPONSE")
    # resp = twiml.messaging_response.MessagingResponse()
    if response == "menu":
        resp.add(plivoxml.MessageElement("StockScraper Commands:\n/start\n/stop\n/mystocks\n/details 'STOCK'\n/price\n/add\n/remove", src=to_number, dst=from_number))
    elif response == "/start":
        StockScraper.start_scraper(stockScraper, stockObjects)
        resp.add(plivoxml.MessageElement("StockScraper has started. You will be notified if an alert is triggered.", src=to_number, dst=from_number))
    elif response == "/stop":
        StockScraper.stop_scraper()
        resp.add(plivoxml.MessageElement("StockScraper has ended. Reply 'start' to begin.", src=to_number, dst=from_number))
    elif response == "/mystocks":
        resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
    elif "/details" in response:
        resp.add(plivoxml.MessageElement(str(stock_price(get_stock_user(response))), src=to_number, dst=from_number))
    elif response == "/add":
        resp.add(plivoxml.MessageElement("Please reply with the stock acronym you would like to add followed by its floor/ceiling.\n\nEx: NOK-1.00-4.50", src=to_number, dst=from_number))
    elif stockAck in StockDictionary.NASDAQ or StockDictionary.COLE and stockFloor and stockCeiling:
        try:
            float(stockFloor)
            float(stockCeiling)
            stockObjects.append(Stock("", "", f"{stockAck}", "", 0.0, stockFloor, stockCeiling))
            resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
        except ValueError or Exception as e:
            print(str(e))
            resp.add(plivoxml.MessageElement("You failed to enter a stock correctly. Type /add to try again.", src=to_number, dst=from_number))
    elif stockAck and not stockFloor or stockCeiling:
        resp.add(plivoxml.MessageElement("You failed to enter a stock correctly. Type /add to try again.", src=to_number, dst=from_number))
    else:
        resp.add(plivoxml.MessageElement("Unrecognized command. Please type 'menu' for help.", src=to_number, dst=from_number))
    print(resp.to_string())
    return Response(resp.to_string(), mimetype='application/xml')


if __name__ == '__main__':
    app.run()
