from src.base.http_client import APIClient
from tests.test_definitions import BaseConfig

client = APIClient(BaseConfig.TESTRAIL_URL, BaseConfig.TESTRAIL_USER, BaseConfig.TESTRAIL_PASSWORD)


def update_test_case(test_run, test_case, status):
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


def get_test_case(test_case):
    case = client.send_get('get_case/' + test_case)
    return case