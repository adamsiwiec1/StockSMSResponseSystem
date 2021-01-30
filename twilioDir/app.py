from flask import Flask, request
from twilio.twiml.messaging_response import Body
from twilio import twiml
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
                string = f"{Stock.acronym} {Stock.price}\nFloor: {Stock.floor}\nCeiling: {Stock.ceiling})"
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
def sms():
    number = request.form['From']
    message_body = request.form['Body']

    print(number)
    print(message_body)
    stockAck = ""
    stockFloor = ""
    stockCeiling = ""

    # Handle new incoming stock
    if "-" in message_body.lower():
        newStock = message_body.rsplit("-", 3)
        stockAck = newStock[0]
        stockFloor = newStock[1]
        stockCeiling = newStock[2]

    resp = twiml.messaging_response.MessagingResponse()
    if message_body or message_body.lower == "menu":
        resp.message("StockScraper Commands:\n/start\n/stop\n/mystocks\n/details 'STOCK'\n/price"
                     "\n/add\n/remove".format(number, message_body))
    elif message_body or message_body.lower == "/start":
        resp.message("StockScraper has started. You will be notified if an alert is triggered.".format(number, message_body))
    elif message_body or message_body.lower == "/stop":
        resp.message("StockScraper has ended. Reply 'start' to begin.".format(number, message_body))
    elif message_body or message_body.lower == "/mystocks":
        resp.message(print_stocks())
    elif "/details" in message_body.lower():
        resp.message(stock_price(get_stock_user(message_body).format(number, message_body)))
    elif message_body.lower() == "/add":
        resp.message("Please reply with the stock acronym you would like to add followed by its floor/ceiling.\n\n"
                     "Ex: NOK-1.00-4.50".format(number, message_body))
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
        resp.message(print_stocks())
    elif stockAck and not stockFloor or stockCeiling:
        resp.message("You failed to enter a stock correctly. Type /add to try again.".format(number, message_body))
    else:
        resp.message("Unrecognized command. Please type 'menu' for help.".format(number, message_body))
    return str(resp)


if __name__ == '__main__':
    app.run()