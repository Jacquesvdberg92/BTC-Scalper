from binance.client import Client 
import time
import key

# API key/secret are required for user data endpoints
client = Client(key.api_key,key.api_secret)

#Symbols
BTCBUSD = 'BTCBUSD'
BTCUSDT = 'BTCUSDT'
BUSDUSDT = 'BUSDUSDT'

#var
delta = 0
size = key.size
diff = key.diff

#logging - NOT IMPLEMENTED YET
#log = open("log.txt", "a")

#functions 
def BTCBUSD_Orderbook(): #gets BTC / BUSD orders
    order = client.get_order_book(symbol = BTCBUSD)
    return order

def BTCUSDT_Orderbook(): #gets BTC / USDTT orders
    order = client.get_order_book(symbol = BTCUSDT)
    return order

def BUSDUSDT_Orderbook(): #gets BUSD / USDT orders
    order = client.get_order_book(symbol = BUSDUSDT)
    return order
#######################################################

#Buy and sell orders
def BTC_BUSD(i): #sells BTC for BUSD and converst to USDT
    q = round((size/i),5)
    order = client.order_market_sell(symbol=BTCBUSD, quantity=q) #Sells BTC for BUSD
    #order = client.order_market_sell(symbol=BUSDUSDT, quantity=size) #Converst BUSD to USDT

def USDT_BTC(i): #buys BTC with USDT
    order = client.order_market_buy(symbol=BTCUSDT, quantity=i) #Buys BTC with USDT

    

def BTC_USDT(i): #sells BTC for USDT and converst to BUSD
    q = round((size/i),5)
    order = client.order_market_sell(symbol=BTCUSDT, quantity=q)
    #order = client.order_market_buy(symbol=BUSDUSDT, quantity=size)

def BUSD_BTC(i): #buys BTC with BUSD
    order = client.order_market_buy(symbol=BTCBUSD, quantity=i)
############################################################

#Main Loop
while(key.loop == 'true'):

    #Sets Target values
    BUSD = BTCBUSD_Orderbook() #BUSD orderbook to work with
    BUSD_Bid = float(BUSD['bids'][0][0]) #Cost of buying BTC with BUSD
    BUSD_Ask = float(BUSD['asks'][0][0]) #Cost of selling BTC for BUSD

    USDT = BTCUSDT_Orderbook() #USDT orderbook to work with
    USDT_Bid = float(USDT['bids'][0][0]) #Cost of buying BTC with USDT
    USDT_Ask = float(USDT['asks'][0][0]) #Cost of selling BTC for USDT



    #Here we check selling to BUSD and Buying with USDT
    delta = round((BUSD_Ask - USDT_Bid),5) #Delta for selling BTC for BUSD and buying BTC with USDT
    print("BTC Selling at: " + str(BUSD_Ask) + " BUSD." 
          + "BTC Buying at: " + str(USDT_Bid) + " USDT." 
          + "Delta is: " + str(delta))
    
    #Execute the Selling of BTC for BUSD and buying of BTC with USDT
    if(delta > diff):
        BTC_BUSD(BUSD_Ask)
        print("BTC sold for BUSD")
        #Safety check to 'ensure' your buying at the 'right' price
        #con = float(BUSDUSDT_Orderbook()['asks'][0][0])
        #safety = float(BTCUSDT_Orderbook()['bids'][0][0])
        safety = float(BTCBUSD_Orderbook()['bids'][0][0])
        while(safety > (BUSD_Ask - 7)):
            safety = float(BTCBUSD_Orderbook()['bids'][0][0])
            #con = float(BUSDUSDT_Orderbook()['asks'][0][0])
        #con = con * size
        BUSD_BTC(round((size/BUSD_Ask),5))
        print("BTC bought with BUSD")
        #USDT_BTC(round((con/safety),5))



    #Execute the Selling of BTC for BUSD and buying of BTC with USDT
    delta = round((USDT_Ask - BUSD_Bid),5)
    print("BTC Selling at: " + str(USDT_Ask) + " USDT." 
          + "BTC Buying at: " + str(BUSD_Bid) + " BUSD." 
          + "Delta is: " + str(delta))

    #Execute the Selling of BTC for USDT and buying of BTC with BUSD    
    if(delta > diff):
        BTC_USDT(USDT_Ask)
        print("BTC sold for USDT")
        #Safety check to 'ensure' your buying at the 'right' price
        #con = float(BUSDUSDT_Orderbook()['bids'][0][0])
        #safety = float(BTCBUSD_Orderbook()['bids'][0][0])
        safety = float(BTCUSDT_Orderbook()['bids'][0][0]) 
        while(safety > (USDT_Ask - 7)):
            safety = float(BTCUSDT_Orderbook()['bids'][0][0])
            #con = float(BUSDUSDT_Orderbook()['bids'][0][0])
        #con = con * size
        USDT_BTC(round((size/USDT_Ask),5))
        print("BTC bought with USDT")
        #BUSD_BTC(round((con/safety),5))
    print("\n" + "####################################################################" + "\n")
    time.sleep(150)

