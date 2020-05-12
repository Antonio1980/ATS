#!/bin/bash

if [[ ! -d ~/Allure/bin/ ]]; then
  # shellcheck disable=SC2242
  exit "You should install Allure locally first."
fi

~/Allure/bin/allure generate ../allure_results/ -o ../allure_reports/ --clean
cp -r ../allure_reports/history ../allure_results/history
~/Allure/bin/allure generate ../allure_results/ -o ../allure_reports/ --clean
