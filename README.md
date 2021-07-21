# CryptoCurrencyPriceTracker
(Code File: main.py)
Live Cryptocurrency tracker for some of the biggest cryptocurrencies on the market.
This is back end coded with python and sqlite and frontend GUI interface also coded with python via Tkinter.Coin Market Cap API is used for extracting data.
User will input his purchased bitcoin name,its cost price and number of coins bought and will receive complete information about all his bitcoin investments like list of bit coin details and net gain or net loss. User will be able to add, delete or update coin information.
User will get alert desktop notifications when his loss is below 10% or gain above 10%.


.py file to .exe file :
import pyinstaller
pyinstaller main.py
pyinstaller main.py --onefile --noconsole --icon=favicon.ico
