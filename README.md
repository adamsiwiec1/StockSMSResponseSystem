# StockSMSResponseSystem

**Overview:** 

To build on my StockScraper alert system, I implemented functionality that allows the user to control the script using text messages. Throughout the process I familiarized myself with two popular VoIP/SMSoIP platforms, Twilio and Plivo. The program allows the user to add stocks to their alert list, start or stop the alert system, and check
the price of any stock by simply sending a text message. The system either replies with confirmation or lets the user know they entered something incorrectly. 

**currently working mainly with Plivo - use that directory to run the app

**Implementation**
- Data retrieved using yfinance API.
https://pypi.org/project/yfinance/

- Used Ngrok to forward requests from Plivo to my local Flask server.<br/>
https://dashboard.ngrok.com/get-started/tutorials <br/>
https://flask.palletsprojects.com/en/1.1.x/ 

Instructions:
1. Run app.py using python.
2. Start ngrok and run: <br/>
 *port = whatever app.py local host is running on*
  ```
  ngrok http 'port'
  ```
3. Copy your ngrok url and configure Plivo (or Twilio).
4. You must repeat step 3 every time you restart ngrok.
5. Assuming app.py is running along with ngrok on the corresponding port, text 'Menu' to your configured Plivo or Twilio phone number.

***************************************************
*Examples*

Text 'Menu' to see all the commands:

![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSMSResponse2.png?raw=true)

Text /details or /price followed by a stock acronym:

![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSmsResponseDetails.png?raw=true)
![alt text](https://github.com/adamsiwiec1/StockSMSResponseSystem/blob/master/etc/StockSMSResponsePrice.png?raw=true)

# Twilio vs Plivo
Twilio's website is user friendly and the libraries for the API are cleaner. Plivo is a bit more transparent. I feel like I have more control using Plivo, both on their website and with their Python API library. I implemented both a PlivoDir and TwilioDir in this project to outline the difference. 

**My choice - Plivo**<br/>
Cheaper - $0.0050/sms w/Plivo vs. 0.0075 w/ Twilio.<br/>
Transparant - less cute, more detailed. <br/>
Drawbacks - you need a business/organizational email to register and it <br/>
can be a bit slower

https://www.twilio.com/

https://www.plivo.com/

**************************************************
Created by Adam Siwiec.

Email: adam2.siwiec@gmail.com

Send me an email with any questions and feel free to clone/improve my code. 
