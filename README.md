# StockSMSResponseSystem

Overview: 

To build on my StockScraper alert system, I implemented functionality that allows the user to control the script using text messages. Throughout the process I familiarized myself with two popular VoIP/SMSoIP, Twilio and Plivo. The program allows the user to add stocks to their alert list, start or stop the alert system, and check
the price of any stock by simply sending a text message. The system either replies with confirmation or lets the user know they entered something incorrectly. 
***************************************************

Built using ngrok and flask:

https://dashboard.ngrok.com/get-started/tutorials

https://flask.palletsprojects.com/en/1.1.x/

Text 'Menu' to see all the commands:

![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSMSResponse2.png?raw=true)

Text /price followed by any stock acronym to receive its current price:

![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSMSResponsePrice.png?raw=true)

# Twilio vs Plivo
Twilio seems to be more user friendly and the libraries for the API are cleaner. Plivo is a bit more transparent. I feel like I have more control using Plivo, both on their website and with their library. I implemented both a PlivoDir and TwilioDir in this project to outline the difference. 

My choice - Plivo

Cheaper - $0.0050/sms w/Plivo vs. 0.0075 w/ Twilio.

Transparant - less cute, more transparent/detailed. 

Negatives? - can be a bit slower and buggy

**************************************************
Created by Adam Siwiec.

Email: adam2.siwiec@gmail.com

Send me an email with any questions and feel free to clone/improve my code. 
