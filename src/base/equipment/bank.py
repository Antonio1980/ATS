from config_definitions import BaseConfig


class Bank(object):

    def __init__(self, customer):
        """
        Constructor for Bank class.
        :param customer: Customer object.
        """
        self.bank_name = "AsBank"
        self.bic = BaseConfig.BIC
        self.iban = BaseConfig.IBAN
        self.clearing_company = "0"
        self.address = customer.street
        self.bank_account = BaseConfig.ACCOUNT
        self.credit_card = self.CreditCard(customer)

    def __repr__(self):
        return "Bank: %s, BIC: %s, IBAN: %s, C. Company: %s, Address: %s" %(self.bank_name, self.bic, self.iban,
                                                                            self.clearing_company, self.address)


    class CreditCard(object):
        
        def __init__(self, customer, mode=None):
            """
            Constructor for CreditCard class.
            :param customer: Customer object.
            :param mode: If some value is provided, CVV = 123 (3D secure).
            """
            self.id = 0
            self.card_currency = "USD"
            self.postal_code = "123456"
            self.personal_id = "669998558"
            self.passport_number = "A5584534"
            self.city = customer.city
            self.phone = customer.phone
            self.email = customer.email
            self.state = customer.state
            self.street = customer.street
            self.country = customer.country
            self.owner_ln = customer.last_name
            self.owner_fn = customer.first_name
            self.phone_prefix = customer.phone_prefix
            self.card_number = BaseConfig.CARD_NUMBER
            self.expiry_year = int(BaseConfig.EXPIRY_YEAR)
            self.expiry_month = int(BaseConfig.EXPIRY_MONTH)
            if mode:
                self.cvv = BaseConfig.CVV2
            else:
                self.cvv = BaseConfig.CVV

        def __repr__(self):
            return "Credit Card ID %d, NUMBER: %s, CVV: %s" %(self.id, self.card_number, self.cvv)
