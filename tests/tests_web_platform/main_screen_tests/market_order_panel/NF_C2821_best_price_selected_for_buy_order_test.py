# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.postman_client import PostmanClient


@test(groups=['market_order_panel', ])
class BestPriceSelectedForBuyOrders(unittest.TestCase):
    def setUp(self):
        self.test_case = '2821'
        self.account_details = Instruments.get_csv_data(BaseConfig.CUSTOMERS_PENDING)[-1][0].split(',')
        self.customer_id = self.account_details[2]
        self.auth_token = self.account_details[5]
        Instruments.customer_approval(self.customer_id)
        PostmanClient.add_balance(self.customer_id, '1', '20000')   #USD currency
        PostmanClient.add_balance(self.customer_id, '3', '2')   #Bitcoin crypto
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.results = BaseConfig.WTP_TESTS_RESULT

    @test(groups=['functional', 'positive', ], depends_on_groups=["sanity", ])
    def test_best_price_selected_for_buy_orders(self):
        step1 = False
        try:
            best_price_and_quantity = Instruments.get_best_price_and_quantity_for_order_buy("1013")
            quantity = best_price_and_quantity[1]
            price = best_price_and_quantity[0]
            order_quantity = round(quantity - (quantity/100*20), 5)
            postman_client = PostmanClient(self.auth_token)
            order_response = postman_client.create_order("1", order_quantity, "1013")
            query_id_trade_crypto = "SELECT id FROM trades_crypto WHERE customerId = " + self.customer_id + " and direction = 'buy';"
            id_trade_crypto = str(Instruments.run_mysql_query(query_id_trade_crypto)[0][0])
            query_price_from_trade = "SELECT price  FROM trades_crypto WHERE id = " + id_trade_crypto + ";"
            price_from_trade = (Instruments.run_mysql_query(query_price_from_trade)[0][0])
            if price_from_trade == price :
                step1 = True
            else:
                step1 = False

        finally:
            if step1 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                Instruments.update_test_case(self.test_run, self.test_case, 0)


