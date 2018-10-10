#!/usr/bin/env bash

timestamp=$(date +"%s")
collection='C:\GitLab\crm_bo_qa\src\repository\ForgotPasswordTests.postman_collection.json'
env='C:\GitLab\crm_bo_qa\src\repository\DX.postman_environment.json'

# create separate outfile for each run
outfile=./reports/logs/outfile-${timestamp}.json

# redirect all output to /dev/null
newman run ${collection} -e ${env} ${outfile} > /dev/null2>&1