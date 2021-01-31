# StockSMSResponseSystem
***************************************************
Overview: To build on my StockScraper alert system, I implemented functionality that allows the user to control the script using text messages. Throughout the process I familiarized myself with two popular VoIP/SMSoIP, Twilio and Plivo. The program allows the user to add stocks to their alert list, start or stop the alert system, and check
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

**In Process of Implementing Sentinel Doubly Linked List in StockAlertsLinkedList branch**

Created by Adam Siwiec.

Email: adam2.siwiec@gmail.com


Description:
**************************************************
Allows the user to enter a stock acronym, price floor, and price ceiling for as many stocks as they would like to monitor. After a user has entered their email address or phone number along with stock details, the script will alert the user using the contact method of their choosing with a description of what is happening. 

Installation Instructions:
**************************************************
1. Download and extract the zip file from StockAlerts repository. 
2. Download/Install Python if you don't already have it. 
3. Right click the alert.py file, choose 'open with', and run the python file using python.exe
4. Follow the directions on CLI to start sending alerts. 

Help:
**************************************************
Send me an email with any questions and feel free to clone/improve my code. 
