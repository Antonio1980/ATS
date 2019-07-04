from src.base.utils.utils import Utils
from src.base import test_token, base_url, api_base_url


class ServiceRoute:
    api_url = api_base_url
    validation_url = base_url + "appProxy/openAccountDx.html"
    redirection_url = base_url + "appProxy/finishDepositVerification.html"
    headers = {'Content-Type': "application/json", 'Authorization': None, 'Test-Token': test_token,
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    (timestamp_from, timestamp_to) = Utils.to_timestamp()
    (date_from, date_to) = Utils.get_dates()
