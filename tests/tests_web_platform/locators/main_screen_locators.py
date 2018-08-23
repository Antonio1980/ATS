class MainScreenLocators(object):
    UPPER_RULER_ID = "dx_header"  # "//*[@id='dx_header']"
    ASSET_PANEL = "//*[@id='dx_platform']//div[@class='assetsSidebar exchange hidden']"
    INSTRUMENT_QUICK_INFO_PANEL = "// *[ @ id = 'exchangeEntity_0']/div[@class = 'infoSection section']/div[@class = 'header']"
    GRAPH_AREA = "//*[@id='exchangeEntity_0']//div[@class='mainChartContainer']"
    MARKET_ORDER_BUTTON = "//*[@id='exchangeEntity_0']//div[@class='tradeType market selected']"
    LIMIT_BUTTON = "//*[@id='exchangeEntity_0']//div[contains(text(),'LIMIT')]"
    MARKET_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm market selected']"
    LIMIT_ORDER_PANEL = "//*[ @ id = 'exchangeEntity_0'] // div[@class='tradeForm limit selected']"
    CURRENT_PORTFOLIO_ID = "zoneContainer_balance"   # "//*[@id='zoneContainer_balance']"
    ORDER_BOOK_PANEL_ID = "zoneContainer_marketInfo"   #"//*[@id='zoneContainer_marketInfo]"
    OPEN_ORDER_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersOpen first selected']"
    ORDERS_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_ordersHistory']"
    TRADES_HISTORY_TABLE = "//*[@id='dxPackageContainer_dx_positions']//div[@class='positionsTab_tradesHistory last']"
    LAST_TRADES_PANEL = "//*[@id='zoneContainer_marketInfo']/div[@class='infoSection lastTrades']"
    LOGO = "//*[@id='dx_header']/div[@class='logo']"
    SIGH_IN_BUTTON = "//*[@id='dx_header']//a[@class='loginButton']"
    SIGH_UP_BUTTON = "//*[@id='dx_header']//a[@class='signUpLink']"
    LANGUAGE_FLAG = "//*[@id='dx_header']//img[@class='flag']"
    MAIN_MENU_ICON = "//*[@id='dx_header']/button[@class='mainMenuIcon']"
    ABOUT = ""
    HELP = ""
    FAQ = ""
    USER_NAME_ON_UPPER_RULER = "//*[@id='dx_header']//div[@class='name']"
    






