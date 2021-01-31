# StockSMSResponseSystem
***************************************************
Overview: 

To build on my StockScraper alert system, I implemented functionality that allows the user to control the script using text messages. Throughout the process I familiarized myself with two popular VoIP/SMSoIP, Twilio and Plivo. The program allows the user to add stocks to their alert list, start or stop the alert system, and check
the price of any stock by simply sending a text message. The system either replies with confirmation or lets the user know they entered something incorrectly. 
***************************************************

If a user texts 'Menu' to the StockSMSResponseSystem:

![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSMSResponse2.png?raw=true)


# Twilio vs Plivo
Twilio seems to be more user friendly and the libraries for the API are much cleaner. Plivo is a bit less cute, but more transparent. I feel like I have more control using Plivo, both on their website and with their library. I implemented both a PlivoDir and TwilioDir in this project to outline the difference. 

My choice? Plivo

Cheaper - $0.0050/sms w/Plivo vs. 0.0075 w/ Twilio.

Transparant - less cute, but more detailed. 

Negatives? - can be a bit slower and buggy

Created by Adam Siwiec.

Email: adam2.siwiec@gmail.com


**************************************************

Send me an email with any questions and feel free to clone/improve my code. 