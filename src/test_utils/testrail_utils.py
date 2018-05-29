# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.http_client import APIClient
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import parse_args


def update_test_case(test_run, test_case, status):
    client = APIClient(BaseConfig.TESTRAIL_URL)
    args = parse_args(test_run)
    case = client.send_get('get_case/' + test_case)
    if status == 1:
        # 'add_result_for_case/'-run, -38 / 2590
        return client.send_post(
            'add_result_for_case/' + test_run + '/' + test_case,
            {'status_id': status, 'comment': 'This test ' + test_case + ' PASSED !'}
        )
    else:
        return client.send_post(
            'add_result_for_case/' + test_run + '/' + test_case,
            {'status_id': status, 'comment': 'This test ' + test_case + ' FAILED !'}
        )
