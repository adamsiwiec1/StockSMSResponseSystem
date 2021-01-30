from flask import Flask, request, make_response, Response
from plivo.rest import phlo_client
from twilio.twiml.messaging_response import Body
import plivo
from plivo import plivoxml
from stockDir.dictionary import StockDictionary
from stockDir.stock import Stock
from stockDir.env import Config as c

# Stock List
stockObjects = [Stock("", "", "", "", 0.0, 0.0, 0.0)]
app = Flask(__name__)


def print_stocks():
    string = ""
    for stock in stockObjects:
        string += str(stock.acronym + f" {stock.price}\n")
    if len(string) < 4:
        string = "You have not added any stocks. Text /add to append."
    return string


def stock_price(ack):
    if ack == "ERROR":
        string = "Error"
    elif ack != "ERROR":
        for stock in stockObjects:
            if stock.acronym.lower() == ack.lower():
                string = f"{stock.acronym} {stock.price}\nFloor: {stock.floor}\nCeiling: {stock.ceiling})"
            else:
                string = "You must enter a stock you have added to /mystocks"
    else:
        string = "You broke the matrix. Try again."

    return string


def get_stock_user(details):
    details.rsplit(" ", 2)
    if len(details[0]) > 7:
        return "ERROR"
    else:
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
        resp.add(plivoxml.MessageElement("StockScraper has started. You will be notified if an alert is triggered.", src=to_number, dst=from_number))
    elif response == "/stop":
        resp.add(plivoxml.MessageElement("StockScraper has ended. Reply 'start' to begin.", src=to_number, dst=from_number))
    elif response == "/mystocks":
        resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
    elif "/details" in response:
        resp.add(plivoxml.MessageElement(stock_price(get_stock_user(response)), src=to_number, dst=from_number))
    elif response == "/add":
        resp.add(plivoxml.MessageElement("Please reply with the stock acronym you would like to add followed by its floor/ceiling.\n\nEx: NOK-1.00-4.50", src=to_number, dst=from_number))
    elif stockAck and stockFloor and stockCeiling and stockAck and stockFloor and stockCeiling and stockAck in StockDictionary.NASDAQ:  # This is really painful I know there's a simpler way ill do it l8tr
        # try:
        #     stockFloor = float(stockFloor)
        #     stockCeiling = float(stockCeiling)
        # except ValueError or TypeError or AttributeError as e:
        #     resp.message(e)
        # if stockFloor and stockCeiling is float:
        stockObjects.append(Stock("", "", f"{stockAck}", "", 0.0, stockFloor, stockCeiling))
        # elif stockFloor and stockCeiling is not float:
        #     resp.message("Your floor and ceiling must be numbers.")
        resp.add(plivoxml.MessageElement(print_stocks(), src=to_number, dst=from_number))
    elif stockAck and not stockFloor or stockCeiling:
        resp.add(plivoxml.MessageElement("You failed to enter a stock correctly. Type /add to try again.", src=to_number, dst=from_number))
    else:
        resp.add(plivoxml.MessageElement("Unrecognized command. Please type 'menu' for help.", src=to_number, dst=from_number))
    print(resp.to_string())
    return Response(resp.to_string(), mimetype='application/xml')


if __name__ == '__main__':
    app.run()
