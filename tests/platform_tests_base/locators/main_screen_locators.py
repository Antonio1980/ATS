UPPER_RULER_ID = "dx_header"  # "//*[@id='dx_header']"
UPPER_RULER = "//*[@id='dx_header']"
"'//*[@id='exchangeEntity_0']//div[@class = 'assetName']"
INSTRUMENT_QUICK_INFO_PANEL = "// *[ @ id = 'exchangeEntity_0']/div[@class = 'infoSection section']/div[@class = 'header']"
GRAPH_AREA = "//*[@id='exchangeEntity_0']//div[@class='mainChartContainer']"
MARKET_ORDER_BUTTON = "//*[@id='exchangeEntity_0']//div[@class='tradeType market selected']"
LIMIT_BUTTON = "//*[@id='exchangeEntity_0']//div[contains(text(),'LIMIT')]"
MARKET_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm market selected']"
LIMIT_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm limit selected']"
CURRENT_PORTFOLIO_ID = "zoneContainer_balance"  # "//*[@id='zoneContainer_balance']"
ORDER_BOOK_PANEL_ID = "zoneContainer_marketInfo"  # "//*[@id='zoneContainer_marketInfo]"
ORDER_BOOK_PANEL = "//*[@id='zoneContainer_marketInfo]"
ORDERS_INFO_PANEL = "//*[@id='dxPackageContainer_dx_positions']"
OPEN_ORDER_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersOpen first selected']"
ORDERS_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersHistory']"
TRADES_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_tradesHistory last']"
LAST_TRADES_PANEL = "//*[@id='zoneContainer_marketInfo']/div[@class='infoSection lastTrades']"
LOGO = "//*[@id='dx_header']/a[@class='logo']"
CRYPTO_BUTTON = "//*[@id='dx_header']//div[@class = 'assetsTypeFilter crypto selected']"
CRYPTO_BUTTON_NOT_SELECTED = "//*[@id='dx_header']//div[@class = 'assetsTypeFilter crypto']"
DIGITAL_STOCKS_BUTTON = "//*[@id='dx_header']//div[@class ='assetsTypeFilter stocks newType']"

SIGH_IN_BUTTON = "//*[@id='dx_header']//a[@class='headerBtn loginButton']"
SIGH_UP_BUTTON = "//*[@id='dx_header']//a[@class='headerBtn signUpLink']"
LANGUAGE_FLAG = "//*[@id='dx_header']//div[@class = 'headerBtn languageContainer flag_en']"
MAIN_MENU_ICON = "//*[@id='dx_header']/button[@class='mainMenuIcon']"
TIME = "//*[@id='dx_header']//div[@class='time']"
DATE = "//*[@id='dx_header']//div[@class='date']"
ABOUT = ""
HELP = ""
FAQ = ""
USER_NAME_ON_UPPER_RULER = "//*[@id='dx_header']//span[@class='name']"
REGISTRATION_FORM = "//*[@id='dxPackageContainer_openAccountDx']//div[@class='registration-form-wrapper']"
SIGN_IN_FORM_ID = "dialogBody"    # "//*[@id='dialogBody']"
USER_PROFILE_PANEL = "//*[@id='dx_myAccount']//div[@class='personalDetails']"
SCREEN_ELEMENTS_UNDER_PROFILE_PANEL_ID = "dxPackageContainer_platform_zones"   # //*[@id='dxPackageContainer_platform_zones']
FUNDS_BUTTON = "//*[@id='dx_header']//div[@class='headerBtn accountStatus_funds']"
TIME_ON_UPPER_RULER = "//*[@id='dx_header']//div[@class = 'time']"
DATE_ON_UPPER_RULER = "//*[@id='dx_header']//div[@class = 'date']"
CURRENT_PORTFOLIO = "//*[@id='zoneContainer_balance']//div[@class='portfolio']"
LOGOUT_BUTTON = "//*[@id='dx_header']//button[@class ='headerBtn logoutButton']"
FUNDS_PANEL_ID = "dx_fundsBalance" # "//*[@id='dx_fundsBalance']"
FUNDS_PANEL_VISIBLE = "//*[@id='dx_fundsBalance'][not(contains(@style,'display: none'))]"
TRADE_SECTION = "//*[@id='exchangeEntity_0']/div[@class='tradeSecttradeion section']"
LEFT_BAR_ASSET_PANEL = "//*[@id='dx_platform']/div[@class='leftBar']"
CURRENT_PORTFOLIO_VALUE = "//*[@id='zoneContainer_balance']//div[@class='fullClear']"

#QJ
FUNDS_VISIBLE = '''return $("[id='dx_header'] div[class= 'headerBtn accountStatus_funds']").is(":visible");'''
USER_NAME_VISIBLE = '''return $("[id='dx_header'] span[class= 'name']").is(":visible");'''
LOGOUT_VISIBLE = '''return $("[id='dx_header'] button[class = 'headerBtn logoutButton']").is(":visible");'''
USER_PROFILE_VISIBLE = '''return $("[id='dx_myAccount'] div[class= 'personalDetails']").is(":visible");'''
ALL_CURRENCIES_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='0']").is(":visible");'''
CRYPTO_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='1']").is(":visible");'''
STOCKS_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='2']").is(":visible");'''
ETFS_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='3']").is(":visible");'''
STO_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='4']").is(":visible");'''
FIAT_BUTTON_JQ = '''return $("[class='currencyTypeFilter'] button[value='5']").is(":visible");'''

# Asset Panel#
ASSET_PANEL = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']"
LEADING_CURRENCY_MENU = "//*[@id='dx_platform']//div[@class='leadingCurrency']"
BTC_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_btc']"
BTC_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_btc selected']"
ETH_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth']"
USDT_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_usdt']"
USD_CURRENCY_SELECTED = ""
USD_DROPDOWN = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_group_stocks assetsTypeFilterGroup']"
USD_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_group']"
ETH_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth selected']"
STOCKS_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth']"
STOCKS_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_eth selected']"
DXEX_CURRENCY_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_dxex']"
DXEX_CURRENCY_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_dxex selected']"
USD_DEFAULT_CURRENCY_DROPDOWN_NOT_SELECTED = "//*[@id='dx_platform']//li[@class='assetsTypeFilter_exchange_group selected']"  # "//*[@id='dx_platform']//span[contains(text(),'USD')]"
SEARCH_BOX = "//*[@class='assetsSidebar exchange hidden']//div[@class = 'searchBox']/input"
SEARCH_TEXT_BOX = "//*[@id='dx_platform']//div[@class='assetsSidebar cfd hidden']//input[@type='text']"
STAR_ICON_FAV = "//div[@class = 'assetsSidebar exchange hidden']//li[@class = 'favorite icon icon-star']"
TWENTY_FOUR_H_CHANGE_NOT_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='rate']"
TWENTY_FOUR_H_CHANGE_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='volume selected desc']"
TWENTY_FOUR_H_VOLUME_NOT_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='rate']"
TWENTY_FOUR_H_VOLUME_SELECTED = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']//li[@class='volume selected desc']"

CURRENCIES_LIST_PANEL = "//*[@id='dx_platform']//div[@class = 'assetsList ps-container']"
ASSET_PRICE_LIST_FOR_ALL = "//*[@id='dx_platform']//div[@class='assetPrice']"

#Maintenance Time
MAINTENANCE_CONTAINER = "//*[@id='tradingPlatform_exchange']/div[@class='maintenanceContainer hidden']"
PORTFOLIO_WHEN_MAINENTENANCE_TIME = "//*[@id='zoneContainer_balance']/div[@class='fullPortfolio hidden']"
MAINTENANCE_TEXT = "//*[@id='tradingPlatform_exchange']/div[3]/div[@class ='maintenanceTitle'][contains(text(),'We are currently down for our daily scheduled maintenance')]"

#asset data
ALL_CURRENCIES = "//*[@class='assetsList ps-container']/ul/li[(not(contains(@style,'display: none')))]"
ALL_FAVORITE_ASSETS = "//*[@class='assetsList ps-container']/ul/li[contains(@class, 'favorite')][(not(contains(@style,'display: none')))]"
ALL_ICONS = "//*[@id='dx_platform']//img"
UNDERLYING_CURRENCY_SELECTED = "//*[@class = 'assetsList ps-container']//div[@class='underlyingCurrency']"
ASSET_TITLE_SELECTED = "//*[@class = 'assetsList ps-container']//div[@class='assetTitle']"
ASSET_NAME = "//*[@id='exchangeEntity_0']//div[@class = 'assetName']"
BASE_CURRENCY_CODE_MARKET_LIST = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//div[@class = 'blockFooter']//span[@class = 'baseCurrencyCode']"
QUOTED_BUY = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//div[@class = 'detailBlock tradingBuy' ]//span[@class = 'currencySymbol']"

QUOTED_SELL = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//div[@class = 'detailBlock tradingSell' ]//span[@class = 'currencySymbol']"
BASE_CURRENCY_CODE_LIMIT_LIST = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//span[@class='baseCurrencyCode']"
CURRENCY_SYMBOL_BUY_LIMIT = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//div[@class = 'detailBlock tradingBuy']//span[@class='currencySymbol']"
CURRENCY_SYMBOL_SELL_LIMIT = "//*[@id='exchangeEntity_0']//div[@class = 'tradeForm limit selected']//div[@class = 'detailBlock tradingSell']//span[@class='currencySymbol']"
QUOTED_CURRENCY_MARKET_INFO_LIST = "//*[@id='zoneContainer_marketInfo']//span[@class = 'quotedCurrency']"
BASE_CURRENCY_MARKET_INFO_BUYERS = "//*[@id='zoneContainer_marketInfo']//div[@class = 'infoSection buyers']//span[@class = 'baseCurrency']"
BASE_CURRENCY_MARKET_INFO_SELLERS = "//*[@id='zoneContainer_marketInfo']//div[@class = 'infoSection sellers']//span[@class = 'baseCurrency']"
VOLUME_24H_DESC_SELECTED_ASSET = "//li[@class='volume selected desc']"
VOLUME_24H_ASC_SELECTED_ASSET = "//li[@class='volume selected asc']"
CHANGE_24H_NOT_SELECTED_ASSET = "//*[@class = 'assetsSidebar exchange hidden']//li[@class = 'rate']"
CHANGE_24H_DESC_SELECTED_ASSET = "//li[@class = 'rate selected desc']"
CHANGE_24H_ASC_SELECTED_ASSET = "//li[@class = 'rate selected asc']"

#quick panel
BASE_RATE_QUICK_PANEL = "//*[@id='exchangeEntity_0']//span[@class='baseRate']"
EMPHASIS_RATE_QUICK_PANEL = "//*[@id='exchangeEntity_0']//span[@class='emphasisRate']"
CHANGE_24_QUICK_PANEL = "//*[@id='exchangeEntity_0']//div[@class='data value']"
VOLUME_24_QUICK_PANEL = "//*[@id='exchangeEntity_0']//div[@class='stat volume']/div[@class='value']"
HIGH_24_QUICK_PANEL = "//*[@id='exchangeEntity_0']//div[@class='stat high']/div[@class='value']"
LOW_24_QUICK_PANEL = "//*[@id='exchangeEntity_0']//div[@class='stat low']/div[@class='value']"
BASE_RATE_ORDER_BOOK = "//*[@id='zoneContainer_marketInfo']//div[@class='assetRateContainer']//span[@class='baseRate']"
EMPHASIS_RATE = "//*[@id='zoneContainer_marketInfo']//div[@class='assetRateContainer']//span[@class='emphasisRate']"
PRICES_FROM_LAST_TRADES_LIST =  "//*[@id='zoneContainer_marketInfo']//div[@class='infoSection lastTrades'][contains(.,'LAST TRADES')]//div[@class='itemsContainerInner']//div[@class='price']"

#JQ
FYS_LAST_TRADE_PRICE_USD = '''return $("li[data-instrumentid = '1092'] div[class = 'usdPrice']").text();'''
NEGATIVE_CHANGE = '''return $("[id='exchangeEntity_0'] div[class='data prefixNegative']").is(":visible");'''

#Funds filters
CURRENCY_NAME_BY_FILTER = "//*[@class='fundsDataRow']/td[@class='fundsCurrencyName']"
FILTER_ALL = "//*[@class='currencyTypeFilter']//button[@value='0']"
FILTER_CRYPTO = "//*[@class='currencyTypeFilter']//button[@value='1']"
FILTER_STOCKS = "//*[@class='currencyTypeFilter']//button[@value='2']"
FILTER_ETFS = "//*[@class='currencyTypeFilter']//button[@value='3']"
FILTER_STO = "//*[@class='currencyTypeFilter']//button[@value='4']"
FILTER_FIAT = "//*[@class='currencyTypeFilter']//button[@value='5']"
