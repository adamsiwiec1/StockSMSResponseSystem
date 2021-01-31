import plivo
import scrape


def started_scraper_message(to_number):
    client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
    message_created = client.messages.create(
        src='+15709985164',
        dst=f'{to_number}',
        text='StockScraper has started. You will be notified if an alert is triggered.'
    )


def send_price(ack, to_number):
    priceMsg = scrape.scrape_price(ack)
    client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
    message_created = client.messages.create(
        src='+15709985164',
        dst=f'{to_number}',
        text=f'{priceMsg}'
    )


def remove_stock(ack, to_number):
    client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
    message_created = client.messages.create(
        src='+15709985164',
        dst=f'{to_number}',
        text=f'{ack} has been removed'
    )

def remove_stock_notfound(ack, to_number):
    client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
    message_created = client.messages.create(
        src='+15709985164',
        dst=f'{to_number}',
        text=f'{ack} was not found in /stocklibrary'
    )


def broke_matrix(to_number):
    client = plivo.RestClient("MAZJZLYTFIMDDHMJZMYZ", "NWMzZTBiZWFjYTMyYTNkNjFkZTI4MTU5ZDIwNzIx")
    message_created = client.messages.create(
        src='+15709985164',
        dst=f'{to_number}',
        text=f'You broke the matrix'
    )