import requests
import time
import math

currencyPair = 'XRPUSD'
currencyPairSecondaryNotation = 'XXRPZUSD'
isNextOperationBuy = True
buyPrice = 0
currentProfit = 0

def getMarketPrice():
    return float(requests.get(f"https://api.cryptowat.ch/markets/kraken/{currencyPair}/price").json().get('result').get('price'))

def getPriceHistory(datapointInterval):
    return requests.post('https://api.kraken.com/0/public/OHLC', data={'pair':currencyPair, 'interval':str(datapointInterval)}).json().get('result').get(currencyPairSecondaryNotation)

def getAssetPriceSummary():
    return requests.get(f"https://api.cryptowat.ch/markets/kraken/{currencyPair}/summary").json()

def getMovingAverage(datapointInterval):
    datapoints = getPriceHistory(datapointInterval)
    average = 0
    count = 0
    for x in datapoints:
        if float(x[4]) != 0:
            average += float(x[4])
            count += 1
    return average / count

def writeProfit():
    global currentProfit
    file = open('profit.txt', 'w')
    file.write(str(currentProfit))
    file.close()

def attemptBuy():
    oneWeekMovingAverage = getMovingAverage(15)
    twoDayMovingAverage = getMovingAverage(5)
    currentMarketPrice = getMarketPrice()
    if twoDayMovingAverage > oneWeekMovingAverage:
        executeBuy()

def attemptSell():
    global buyPrice
    oneWeekMovingAverage = getMovingAverage(15)
    twoDayMovingAverage = getMovingAverage(5)
    currentMarketPrice = getMarketPrice()
    print(f"attempting to sell. {currentMarketPrice}")
    if twoDayMovingAverage < oneWeekMovingAverage:
        executeSell()
    if currentMarketPrice >= buyPrice*1.02 or currentMarketPrice <= buyPrice*0.99:
        executeSell()
def executeBuy():
    global isNextOperationBuy
    global buyPrice
    buyPrice = getMarketPrice()
    print(f"BUY!!! {buyPrice}")
    isNextOperationBuy = False

def executeSell():
    global isNextOperationBuy
    global buyPrice
    global currentProfit
    marketPrice = getMarketPrice()
    print(f"SELL!!! {marketPrice}")
    currentProfit += marketPrice - buyPrice
    writeProfit()
    isNextOperationBuy = True

def runBot():
    while True:
        if isNextOperationBuy == True:
            attemptBuy()
        else:
            attemptSell()
        time.sleep(60)

runBot()
