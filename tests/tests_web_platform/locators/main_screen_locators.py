UPPER_RULER_ID = "dx_header"  # "//*[@id='dx_header']"

INSTRUMENT_QUICK_INFO_PANEL = "// *[ @ id = 'exchangeEntity_0']/div[@class = 'infoSection section']/div[@class = 'header']"
GRAPH_AREA = "//*[@id='exchangeEntity_0']//div[@class='mainChartContainer']"
MARKET_ORDER_BUTTON = "//*[@id='exchangeEntity_0']//div[@class='tradeType market selected']"
LIMIT_BUTTON = "//*[@id='exchangeEntity_0']//div[contains(text(),'LIMIT')]"
MARKET_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm market selected']"
LIMIT_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm limit selected']"
CURRENT_PORTFOLIO_ID = "zoneContainer_balance"  # "//*[@id='zoneContainer_balance']"
ORDER_BOOK_PANEL_ID = "zoneContainer_marketInfo"  # "//*[@id='zoneContainer_marketInfo]"
OPEN_ORDER_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersOpen first selected']"
ORDERS_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersHistory']"
TRADES_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_tradesHistory last']"
LAST_TRADES_PANEL = "//*[@id='zoneContainer_marketInfo']/div[@class='infoSection lastTrades']"
LOGO = "//*[@id='dx_header']/div[@class='logo']"
SIGH_IN_BUTTON = "//*[@id='dx_header']//a[@class='headerBtn loginButton']"
SIGH_UP_BUTTON = "//*[@id='dx_header']//a[@class='headerBtn signUpLink']"
LANGUAGE_FLAG = "//*[@id='dx_header']//img[@class='flag']"
MAIN_MENU_ICON = "//*[@id='dx_header']/button[@class='mainMenuIcon']"
ABOUT = ""
HELP = ""
FAQ = ""
USER_NAME_ON_UPPER_RULER = "//*[@id='dx_header']//span[@class='name']"
REGISTRATION_FORM = "//*[@id='dxPackageContainer_openAccountDx']//div[@class='registration-form-wrapper']"
SIGN_IN_FORM_ID = "dialogBody"    #"//*[@id='dialogBody']"
USER_PROFILE_PANEL = "//*[@id='dx_myAccount']//div[@class='personalDetails']"
SCREEN_ELEMENTS_UNDER_PROFILE_PANEL_ID = "dxPackageContainer_platform_zones"   #//*[@id='dxPackageContainer_platform_zones']
FUNDS_BUTTON = "//*[@id='dx_header']//div[@class='headerBtn accountStatus_funds']"
TIME_ON_UPPER_RULER = "//*[@id='dx_header']//div[@class = 'time']"
DATE_ON_UPPER_RULER = "//*[@id='dx_header']//div[@class = 'date']"
CURRENT_PORTFOLIO = "//*[@id='zoneContainer_balance']//div[@class='portfolio']"
LOGOUT_BUTTON = "//*[@id='dx_header']//button[@class ='headerBtn logoutButton']"
FUNDS_PANEL_ID = "dx_fundsBalance" #"//*[@id='dx_fundsBalance']"




#Asset Panel#
ASSET_PANEL = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']"
LEADING_CURRENCY_MENU = "//*[@id='dx_platform']//div[@class='leadingCurrency']"
BTC_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_btc']"
BTC_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_btc selected']"
ETH_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth']"
ETH_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth selected']"
DXEX_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_dxex']"
DXEX_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_dxex selected']"
USD_DEFAULT_CURRENCY_DROPDOWN_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_group']"                      #"//*[@id='dx_platform']//span[contains(text(),'USD')]"
SEARCH_BOX = "//*[@id='dx_platform']/div[1]/div[2]/div[2]"
SEARCH_TEXT_BOX = "//*[@id='dx_platform']//div[@class='assetsSidebar cfd hidden']//input[@type='text']"
STAR_ICON_FAV = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@title='Fav']"
TWENTY_FOUR_H_CHANGE_NOT_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='volume']"
TWENTY_FOUR_H_CHANGE_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='volume selected desc']"
TWENTY_FOUR_H_VOLUME_NOT_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='rate']"
TWENTY_FOUR_H_VOLUME_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='rate selected desc']"
CURRENCIES_LIST_PANEL = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']/div[@class='assetsList ps-container']/ul"


# when BTC currency is selected, no one is favorite
BTC_BITCOIN_CASH_BCH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1024']"
BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[@class='assetChange24h']"
BTC_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[@class='commonPrice']"
BTC_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[@class='usdPrice']"
BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[@class='volumeValue']"
BTC_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1024']" \
                                                               "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_BITCOIN_CASH_BCH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//img[@title='BCH']"
BTC_BITCOIN_CASH_BCH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[contains(text(),'Bitcoin Cash')]"
BTC_BITCOIN_CASH_BCH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[contains(text(),'BCH')]"
BTC_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1024']//div[@class='dot']"


BTC_DASH_DASH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1038']"
BTC_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='assetChange24h']"
BTC_DASH_DASH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='commonPrice']"
BTC_DASH_DASH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='usdPrice']"
BTC_DASH_DASH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='volumeValue']"
BTC_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1038']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_DASH_DASH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//img[@title='DASH']"
BTC_DASH_DASH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[contains(text(),'DASH')]"
BTC_DASH_DASH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='assetTitle'][contains(text(),'DASH')]"
BTC_DASH_DASH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1038']//div[@class='dot']"


BTC_DX_COIN_DXEX_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1032']"
BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[@class='assetChange24h']"
BTC_DX_COIN_DXEX_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[@class='commonPrice']"
BTC_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[@class='usdPrice']"
BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[@class='volumeValue']"
BTC_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1032']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_DX_COIN_DXEX_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//img[@title='DXEX']"
BTC_DX_COIN_DXEX_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[contains(text(),'DX Coin')]"
BTC_DX_COIN_DXEX_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[contains(text(),'DXEX')]"
BTC_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1032']//div[@class='dot']"



BTC_ETHEREUM_ETH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1023']"
BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[@class='assetChange24h']"
BTC_ETHEREUM_ETH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[@class='commonPrice']"
BTC_ETHEREUM_ETH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[@class='usdPrice']"
BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[@class='volumeValue']"
BTC_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1023']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_ETHEREUM_ETH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//img[@title='ETH']"
BTC_ETHEREUM_ETH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[contains(text(),'Ethereum')]"
BTC_ETHEREUM_ETH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[contains(text(),'ETH')]"
BTC_ETHEREUM_ETH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1023']//div[@class='dot']"


BTC_LITECOIN_LTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1026']"
BTC_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[@class='assetChange24h']"
BTC_LITECOIN_LTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[@class='commonPrice']"
BTC_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[@class='usdPrice']"
BTC_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[@class='volumeValue']"
BTC_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1026']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_LITECOIN_LTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//img[@title='LTC']"
BTC_LITECOIN_LTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[contains(text(),'Litecoin')]"
BTC_LITECOIN_LTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[contains(text(),'LTC')]"
BTC_LITECOIN_LTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1026']//div[@class='dot']"


BTC_RIPPLE_XRP_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1025']"
BTC_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[@class='assetChange24h']"
BTC_RIPPLE_XPR_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[@class='commonPrice']"
BTC_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[@class='usdPrice']"
BTC_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[@class='volumeValue']"
BTC_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY =  "//*[@id='dx_platform']//li[@data-instrumentid='1025']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'BTC')]"
BTC_RIPPLE_XRP_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//img[@title='XRP']"
BTC_RIPPLE_XRP_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[contains(text(),'Ripple')]"
BTC_RIPPLE_XRP_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[contains(text(),'XRP')]"
BTC_RIPPLE_XRP_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1025']//div[@class='dot']"

# when DXEX currency is selected, no one is favorite
DXEX_BITCOIN_CASH_BCH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1011']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[@class='assetChange24h']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[@class='commonPrice']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[@class='usdPrice']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[@class='volumeValue']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1011']" \
                                                               "//div[@class='underlyingCurrency'][contains(text(),'DXEX')]"
DXEX_BITCOIN_CASH_BCH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//img[@title='BCH']"
DXEX_BITCOIN_CASH_BCH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[contains(text(),'Bitcoin Cash')]"
DXEX_BITCOIN_CASH_BCH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[contains(text(),'BCH')]"
DXEX_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1011']//div[@class='dot']"


DXEX_DASH_DASH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1040']"
DXEX_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='assetChange24h']"
DXEX_DASH_DASH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='commonPrice']"
DXEX_DASH_DASH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='usdPrice']"
DXEX_DASH_DASH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='volumeValue']"
DXEX_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1040']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'DXEX')]"
DXEX_DASH_DASH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//img[@title='DASH']"
DXEX_DASH_DASH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[contains(text(),'DASH')]"
DXEX_DASH_DASH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='assetTitle'][contains(text(),'DASH')]"
DXEX_DASH_DASH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1040']//div[@class='dot']"


DXEX_LITECOIN_LTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1035']"
DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[@class='assetChange24h']"
DXEX_LITECOIN_LTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[@class='commonPrice']"
DXEX_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[@class='usdPrice']"
DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[@class='volumeValue']"
DXEX_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1035']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'DXEX')]"
DXEX_LITECOIN_LTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//img[@title='LTC']"
DXEX_LITECOIN_LTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[contains(text(),'Litecoin')]"
DXEX_LITECOIN_LTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[contains(text(),'LTC')]"
DXEX_LITECOIN_LTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1035']//div[@class='dot']"


DXEX_RIPPLE_XRP_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1034']"
DXEX_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[@class='assetChange24h']"
DXEX_RIPPLE_XPR_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[@class='commonPrice']"
DXEX_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[@class='usdPrice']"
DXEX_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[@class='volumeValue']"
DXEX_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY =  "//*[@id='dx_platform']//li[@data-instrumentid='1034']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'DXEX')]"
DXEX_RIPPLE_XRP_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//img[@title='XRP']"
DXEX_RIPPLE_XRP_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[contains(text(),'Ripple')]"
DXEX_RIPPLE_XRP_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[contains(text(),'XRP')]"
DXEX_RIPPLE_XRP_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1034']//div[@class='dot']"


# when ETH currency is selected, no one is favorite
ETH_BITCOIN_CASH_BCH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1027']"
ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[@class='assetChange24h']"
ETH_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[@class='commonPrice']"
ETH_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[@class='usdPrice']"
ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[@class='volumeValue']"
ETH_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1027']" \
                                                               "//div[@class='underlyingCurrency'][contains(text(),'ETH')]"
ETH_BITCOIN_CASH_BCH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//img[@title='BCH']"
ETH_BITCOIN_CASH_BCH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[contains(text(),'Bitcoin Cash')]"
ETH_BITCOIN_CASH_BCH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[contains(text(),'BCH')]"
ETH_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1027']//div[@class='dot']"


ETH_DASH_DASH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1039']"
ETH_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='assetChange24h']"
ETH_DASH_DASH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='commonPrice']"
ETH_DASH_DASH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='usdPrice']"
ETH_DASH_DASH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='volumeValue']"
ETH_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1039']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'ETH')]"
ETH_DASH_DASH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//img[@title='DASH']"
ETH_DASH_DASH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[contains(text(),'DASH')]"
ETH_DASH_DASH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='assetTitle'][contains(text(),'DASH')]"
ETH_DASH_DASH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1039']//div[@class='dot']"


ETH_DX_COIN_DXEX_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1033']"
ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[@class='assetChange24h']"
ETH_DX_COIN_DXEX_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[@class='commonPrice']"
ETH_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[@class='usdPrice']"
ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[@class='volumeValue']"
ETH_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1033']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'ETH')]"
ETH_DX_COIN_DXEX_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//img[@title='DXEX']"
ETH_DX_COIN_DXEX_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[contains(text(),'DX Coin')]"
ETH_DX_COIN_DXEX_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[contains(text(),'DXEX')]"
ETH_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1033']//div[@class='dot']"


ETH_LITECOIN_LTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1029']"
ETH_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[@class='assetChange24h']"
ETH_LITECOIN_LTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[@class='commonPrice']"
ETH_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[@class='usdPrice']"
ETH_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[@class='volumeValue']"
ETH_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1029']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'ETH')]"
ETH_LITECOIN_LTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//img[@title='LTC']"
ETH_LITECOIN_LTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[contains(text(),'Litecoin')]"
ETH_LITECOIN_LTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[contains(text(),'LTC')]"
ETH_LITECOIN_LTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1029']//div[@class='dot']"


ETH_RIPPLE_XRP_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1028']"
ETH_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[@class='assetChange24h']"
ETH_RIPPLE_XPR_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[@class='commonPrice']"
ETH_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[@class='usdPrice']"
ETH_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[@class='volumeValue']"
ETH_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY =  "//*[@id='dx_platform']//li[@data-instrumentid='1028']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'ETH')]"
ETH_RIPPLE_XRP_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//img[@title='XRP']"
ETH_RIPPLE_XRP_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[contains(text(),'Ripple')]"
ETH_RIPPLE_XRP_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[contains(text(),'XRP')]"
ETH_RIPPLE_XRP_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1028']//div[@class='dot']"


# when USD currency is selected, no one is favorite
USD_BITCOIN_CASH_BCH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1015']"
USD_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[@class='assetChange24h']"
USD_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[@class='commonPrice']"
USD_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[@class='usdPrice']"
USD_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[@class='volumeValue']"
USD_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1015']" \
                                                               "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_BITCOIN_CASH_BCH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//img[@title='BCH']"
USD_BITCOIN_CASH_BCH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[contains(text(),'Bitcoin Cash')]"
USD_BITCOIN_CASH_BCH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[contains(text(),'BCH')]"
USD_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1015']//div[@class='dot']"


USD_DASH_DASH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1003']"
USD_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='assetChange24h']"
USD_DASH_DASH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='commonPrice']"
USD_DASH_DASH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='usdPrice']"
USD_DASH_DASH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='volumeValue']"
USD_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1003']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_DASH_DASH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//img[@title='DASH']"
USD_DASH_DASH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[contains(text(),'DASH')]"
USD_DASH_DASH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='assetTitle'][contains(text(),'DASH')]"
USD_DASH_DASH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1003']//div[@class='dot']"


USD_BITCOIN_BTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1008']"
USD_BITCOIN_BTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[@class='assetChange24h']"
USD_BITCOIN_BTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[@class='commonPrice']"
USD_BITCOIN_BTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[@class='usdPrice']"
USD_BITCOIN_BTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[@class='volumeValue']"
USD_BITCOIN_BTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1008']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_BITCOIN_BTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//img[@title='BTC']"
USD_BITCOIN_BTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[contains(text(),'Bitcoin')]"
USD_BITCOIN_BTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[contains(text(),'BTC')]"
USD_BITCOIN_BTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1008']//div[@class='dot']"


USD_DX_COIN_DXEX_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1030']"
USD_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[@class='assetChange24h']"
USD_DX_COIN_DXEX_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[@class='commonPrice']"
USD_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[@class='usdPrice']"
USD_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[@class='volumeValue']"
USD_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1030']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_DX_COIN_DXEX_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//img[@title='DXEX']"
USD_DX_COIN_DXEX_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[contains(text(),'DX Coin')]"
USD_DX_COIN_DXEX_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[contains(text(),'DXEX')]"
USD_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1030']//div[@class='dot']"


USD_ETHEREUM_ETH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1014']"
USD_ETHEREUM_ETH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[@class='assetChange24h']"
USD_ETHEREUM_ETH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[@class='commonPrice']"
USD_ETHEREUM_ETH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[@class='usdPrice']"
USD_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[@class='volumeValue']"
USD_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1014']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_ETHEREUM_ETH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//img[@title='ETH']"
USD_ETHEREUM_ETH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[contains(text(),'Ethereum')]"
USD_ETHEREUM_ETH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[contains(text(),'ETH')]"
USD_ETHEREUM_ETH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1014']//div[@class='dot']"


USD_LITECOIN_LTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1017']"
USD_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[@class='assetChange24h']"
USD_LITECOIN_LTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[@class='commonPrice']"
USD_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[@class='usdPrice']"
USD_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[@class='volumeValue']"
USD_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1017']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_LITECOIN_LTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//img[@title='LTC']"
USD_LITECOIN_LTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[contains(text(),'Litecoin')]"
USD_LITECOIN_LTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[contains(text(),'LTC')]"
USD_LITECOIN_LTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1017']//div[@class='dot']"


USD_RIPPLE_XRP_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1016']"
USD_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[@class='assetChange24h']"
USD_RIPPLE_XPR_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[@class='commonPrice']"
USD_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[@class='usdPrice']"
USD_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[@class='volumeValue']"
USD_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY =  "//*[@id='dx_platform']//li[@data-instrumentid='1016']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'USD')]"
USD_RIPPLE_XRP_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//img[@title='XRP']"
USD_RIPPLE_XRP_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[contains(text(),'Ripple')]"
USD_RIPPLE_XRP_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[contains(text(),'XRP')]"
USD_RIPPLE_XRP_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1016']//div[@class='dot']"


# when EUR currency is selected, no one is favorite
EUR_BITCOIN_CASH_BCH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1020']"
EUR_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[@class='assetChange24h']"
EUR_BITCOIN_CASH_BCH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[@class='commonPrice']"
EUR_BITCOIN_CASH_BCH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[@class='usdPrice']"
EUR_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[@class='volumeValue']"
EUR_BITCOIN_CASH_BCH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1020']" \
                                                               "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_BITCOIN_CASH_BCH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//img[@title='BCH']"
EUR_BITCOIN_CASH_BCH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[contains(text(),'Bitcoin Cash')]"
EUR_BITCOIN_CASH_BCH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[contains(text(),'BCH')]"
EUR_BITCOIN_CASH_BCH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1020']//div[@class='dot']"


EUR_DASH_DASH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1037']"
EUR_DASH_DASH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='assetChange24h']"
EUR_DASH_DASH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='commonPrice']"
EUR_DASH_DASH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='usdPrice']"
EUR_DASH_DASH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='volumeValue']"
EUR_DASH_DASH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1037']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_DASH_DASH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//img[@title='DASH']"
EUR_DASH_DASH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[contains(text(),'DASH')]"
EUR_DASH_DASH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='assetTitle'][contains(text(),'DASH')]"
EUR_DASH_DASH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1037']//div[@class='dot']"


EUR_BITCOIN_BTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1018']"
EUR_BITCOIN_BTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[@class='assetChange24h']"
EUR_BITCOIN_BTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[@class='commonPrice']"
EUR_BITCOIN_BTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[@class='usdPrice']"
EUR_BITCOIN_BTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[@class='volumeValue']"
EUR_BITCOIN_BTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1018']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_BITCOIN_BTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//img[@title='BTC']"
EUR_BITCOIN_BTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[contains(text(),'Bitcoin')]"
EUR_BITCOIN_BTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[contains(text(),'BTC')]"
EUR_BITCOIN_BTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1018']//div[@class='dot']"


EUR_DX_COIN_DXEX_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1031']"
EUR_DX_COIN_DXEX_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[@class='assetChange24h']"
EUR_DX_COIN_DXEX_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[@class='commonPrice']"
EUR_DX_COIN_DXEX_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[@class='usdPrice']"
EUR_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[@class='volumeValue']"
EUR_DX_COIN_DXEX_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1031']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_DX_COIN_DXEX_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//img[@title='DXEX']"
EUR_DX_COIN_DXEX_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[contains(text(),'DX Coin')]"
EUR_DX_COIN_DXEX_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[contains(text(),'DXEX')]"
EUR_DX_COIN_DXEX_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1031']//div[@class='dot']"


EUR_ETHEREUM_ETH_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1019']"
EUR_ETHEREUM_ETH_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[@class='assetChange24h']"
EUR_ETHEREUM_ETH_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[@class='commonPrice']"
EUR_ETHEREUM_ETH_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[@class='usdPrice']"
EUR_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[@class='volumeValue']"
EUR_ETHEREUM_ETH_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1019']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_ETHEREUM_ETH_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//img[@title='ETH']"
EUR_ETHEREUM_ETH_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[contains(text(),'Ethereum')]"
EUR_ETHEREUM_ETH_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[contains(text(),'ETH')]"
EUR_ETHEREUM_ETH_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1019']//div[@class='dot']"


EUR_LITECOIN_LTC_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1022']"
EUR_LITECOIN_LTC_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[@class='assetChange24h']"
EUR_LITECOIN_LTC_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[@class='commonPrice']"
EUR_LITECOIN_LTC_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[@class='usdPrice']"
EUR_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[@class='volumeValue']"
EUR_LITECOIN_LTC_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1022']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_LITECOIN_LTC_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//img[@title='LTC']"
EUR_LITECOIN_LTC_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[contains(text(),'Litecoin')]"
EUR_LITECOIN_LTC_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[contains(text(),'LTC')]"
EUR_LITECOIN_LTC_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1022']//div[@class='dot']"


EUR_RIPPLE_XRP_CURRENCY = "//*[@id='dx_platform']//li[@data-instrumentid='1021']"
EUR_RIPPLE_XPR_CURRENCY_24_HOUR_CHANGE_PERCENTAGE = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[@class='assetChange24h']"
EUR_RIPPLE_XPR_CURRENCY_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[@class='commonPrice']"
EUR_RIPPLE_XPR_CURRENCY_USD_LAST_PRICE = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[@class='usdPrice']"
EUR_RIPPLE_XRP_CURRENCY_24_HOUR_VOLUME = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[@class='volumeValue']"
EUR_RIPPLE_XPR_CURRENCY_24_HOUR_VOLUME_QUOTED_CURRENCY =  "//*[@id='dx_platform']//li[@data-instrumentid='1021']" \
                                                        "//div[@class='underlyingCurrency'][contains(text(),'EUR')]"
EUR_RIPPLE_XRP_CURRENCY_SYMBOL = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//img[@title='XRP']"
EUR_RIPPLE_XRP_CURRENCY_NAME = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[contains(text(),'Ripple')]"
EUR_RIPPLE_XRP_CURRENCY_CODE = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[contains(text(),'XRP')]"
EUR_RIPPLE_XRP_CURRENCY_FAV_CIRCLE = "//*[@id='dx_platform']//li[@data-instrumentid='1021']//div[@class='dot']"







