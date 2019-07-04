USD = "//li[@class = 'assetsTypeFilter_exchange_group selected']/span[@class='dynamicFilter']"
IMAGE_USD = "//*[@class='filterImage usd']"
ASSET_BCH = "//*[@data-instrumentid='1024']//img"
USD_ASSETS = "//div[@class='content']/span[@class='currencySymbol'][contains(.,'USD')]"
BCH_ASSETS = "//div[@class='content']/span[@class='currencySymbol'][contains(.,'BCH')]"
USD_OPTION_FROM_USD_DROPDOWN = "//*[@class='assetsGroupTypeFilter_exchange_usd']"
EUR_OPTION_FROM_USD_DROPDOWN = "//*[@class='assetsGroupTypeFilter_exchange_eur']"
JPY_OPTION_FROM_USD_DROPDOWN = "//*[@class='assetsTypeFilter_exchange_jpy']"
BTC_USD_INSTRUMENT = "//*[@id='dx_platform']//div[@class= 'assetsList ps-container ps-active-y']//li[@data-instrumentid = '1013']"
DXCASH_USD_INSTRUMENT_IMG = "//*[@id='dx_platform']//li[@data-instrumentid = '1030']//img[@class = 'assetIcon'][@title = 'DXCASH']"
DXCASH_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'DXCASH/USD')]"
DXCASH_JPY_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'DXCASH/JPY')]"
LTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'LTC/USD')]"
ETH_EUR_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'ETH/EUR')]"
BTC_USD_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'BTC/USD')]"
ETH_JPY_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL = "//*[@id='exchangeEntity_0']//div[@class='assetName'][contains(.,'ETH/JPY')]"
MARKET_TAB_SELECTED = "//*[@id='exchangeEntity_0']//div[@class='tradeType market selected']"
MARKET_TAB = "//*[@id='exchangeEntity_0']//div[@class='tradeType market']"
ESTIMATED_PRICE_FOR_BUY_MARKET ="//*[@id='exchangeEntity_0']//div[@class='tradeBtn buyButton']//div[@class = 'price']"
ESTIMATED_PRICE_FOR_SELL_MARKET = "//*[@id='exchangeEntity_0']//div[@class='tradeBtn sellButton']//div[@class = 'price']"
AMOUNT_FOR_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//input[@class = 'amount']"
VALUE_AVAILABLE_FOR_TRADING_BUY ="//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//span[@class = 'amount']"
AMOUNT_FOR_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//input[@class = 'amount']"
VALUE_AVAILABLE_FOR_TRADING_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//span[@class = 'amount']"
BUY_BUTTON = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']// div[@ class = 'tradeBtn buyButton']"
SELL_BUTTON = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']// div[@ class = 'tradeBtn sellButton']"
AVAILABLE_FOR_TRADING_FUNDS_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//div[@class = 'availableTrading']"
ENTER_AMOUNT_WITH_DEFAULT_0_BUY  = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//input[@type = 'text'][@placeholder = '0']"
MINIMUM_ORDER_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//div[@class = 'amount_error belowMinimum hidden']"
PERCENTAGE_SELECTOR_15_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//button[@value = '15']"
PERCENTAGE_SELECTOR_25_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//button[@value = ' 25']"
PERCENTAGE_SELECTOR_35_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//button[@value = ' 35']"
PERCENTAGE_SELECTOR_50_BUY = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//button[@value = ' 50']"
AVAILABLE_FOR_TRADING_FUNDS_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//div[@class = 'availableTrading']"
ENTER_AMOUNT_WITH_DEFAULT_0_SELL  = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//input[@type = 'text'][@placeholder = '0']"
MINIMUM_ORDER_AMOUNT_MESSAGE_UNDER_ENTER_AMOUNT_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewBuy']//div[@class = 'amount_error belowMinimum hidden']"
PERCENTAGE_SELECTOR_15_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//button[@value = '15']"
PERCENTAGE_SELECTOR_25_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//button[@value = ' 25']"
PERCENTAGE_SELECTOR_35_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//button[@value = ' 35']"
PERCENTAGE_SELECTOR_50_SELL = "//*[@id='exchangeEntity_0']//div[@class='tradeForm market selected']//div[@class ='tradingOverviewSection tradingOverviewSell']//button[@value = ' 50']"
FUNDS_BUTTON = "//*[@id='dx_header']//div[@class = 'headerBtn accountStatus_funds' ]"
USD_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE = "//*[@id='1']//td[@class = 'fundsAvailableBalance']"
BTC_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE = "//*[@id='3']//td[@class = 'fundsAvailableBalance']"
SCROLL_ASSET_PANEL = "//*[@id='dx_platform']//div[@class = 'assetsList ps-container ps-active-y']//div[@class = 'ps-scrollbar-y']"

# jquery locators
VALUE_AVAILABLE_FOR_TRADING_BUY_AFTER_BUFFER = '''return $("[id='exchangeEntity_0'] div[class='tradeForm market selected'] div[class ='tradingOverviewSection tradingOverviewBuy'] span[class='value']").text();'''
VALUE_AVAILABLE_FOR_TRADING_SELL_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeForm market selected'] div[class='tradingOverviewSection tradingOverviewSell'] span[class='amount']").text();'''
VALUE_AVAILABLE_FOR_TRADING_BUY_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeForm market selected'] div[class='tradingOverviewSection tradingOverviewBuy'] span[class='amount']").text(); '''
ESTIMATED_PRICE_FOR_BUY_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeBtn buyButton'] div[class= 'price']").text();'''
ESTIMATED_PRICE_FOR_SELL_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeBtn sellButton'] div[class = 'price']").text();'''
USD_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ = '''return $("[id='1'] td[class = 'fundsAvailableBalance']").text();'''
EUR_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ = '''return $("[id='2'] td[class = 'fundsAvailableBalance']").text();'''
BTC_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ = '''return $("[id='3'] td[class = 'fundsAvailableBalance']").text();'''
ETH_CURRENCY_AVAILBLE_BALANS_FUNDS_PAGE_JQ = '''return $("[id='4'] td[class = 'fundsAvailableBalance']").text();'''
AMOUNT_FOR_BUY_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeForm market selected'] div[class ='tradingOverviewSection tradingOverviewBuy'] input[class = 'amount']").val();'''
AMOUNT_FOR_SELL_JQ = '''return $("[id='exchangeEntity_0'] div[class='tradeForm market selected'] div[class ='tradingOverviewSection tradingOverviewSell'] input[class = 'amount']").val();'''
EUR_FROZEN_BALANS_FUNDS_PAGE_JQ = '''return $("[id='2'] td[class = 'fundsFrozen']").text();'''
BTC_FROZEN_BALANS_FUNDS_PAGE_JQ = '''return $("[id='3'] td[class = 'fundsFrozen']").text();'''
# OrderBook locators
ORDER_BOOK_ENTITIES_SELLERS = "//*[@id='zoneContainer_marketInfo']/div[@class='infoSection sellers']//div[@class='price']"
ORDER_BOOK_ENTITIES_BUYERS = "//*[@id='zoneContainer_marketInfo']/div[@class='infoSection buyers']//div[@class='price']"
