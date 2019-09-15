from datetime import datetime
from src.base import base_url
from src.base.automation_error import AutomationError
from src.base.utils.utils import Utils


class RequestSchema(object):
    validation_url = base_url + "/appProxy/openAccountDx.html"
    redirection_url = base_url + "/appProxy/finishDepositVerification.html"
    forgot_proxy = "/forgotPasswordDx.html?lang=en"
    forgot_password_page_url = base_url + forgot_proxy
    (timestamp_from, timestamp_to) = Utils.to_timestamp()
    (date_from, date_to) = Utils.get_dates()
    edit_date = datetime.utcnow().strftime("%Y-%m-%d")

    def __init__(self):
        super(RequestSchema, self).__init__()

    def __getattr__(self, name):
        if not hasattr(self, name):
            raise AutomationError('{!r} object has no attribute {!r}'.format(self.__class__, name))
        return getattr(self, name)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               ', '.join("{k}={v}".format(k=k[1:], v=self.__dict__[k])
                                         for k in sorted(self.__dict__.keys())))

    def to_json(self):
        return Utils.to_json(self)

    @staticmethod
    def convert(list_):
        return '&'.join(map(str, list_))


class ApiRequestSchema(RequestSchema):
    def __init__(self):
        super(ApiRequestSchema, self).__init__()
        self.jsonrpc = "2.0"
        self.params = list()


class CrmRequestSchema(RequestSchema):
    def __init__(self):
        super(CrmRequestSchema, self).__init__()
        self.body = list()

    def __repr__(self):
        return self.convert(self.body)
