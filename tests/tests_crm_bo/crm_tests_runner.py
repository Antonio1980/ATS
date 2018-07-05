# !/usr/bin/env python
# -*- coding: utf8 -*-


# python wtp_tests_runner.py --group=smoke
# python wtp_tests_runner.py --show-plan
# @test(depends_on=[LogInTest])
# @test(groups=["sanity", "registration_ddt_test"], depends_on=[full_registration_flow_test])
# @test(groups=["sanity", "registration_ddt_test"], depends_on_groups=["smoke"])
def run_tests():
    from proboscis import TestProgram
    from tests.tests_crm_bo import crm_tests_container
    #from tests.tests_web_platform.forgot_password_tests import C3558_forgot_password_ui_test
    #from tests.tests_web_platform.signin_tests import C3690_login_test
    #from tests.tests_web_platform.registration_tests import full_registration_flow_test

    # Run Proboscis and exit.
    TestProgram().run_and_exit()

if __name__ == '__main__':
    run_tests()