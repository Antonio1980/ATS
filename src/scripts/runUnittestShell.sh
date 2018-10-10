#!/usr/bin/env bash


filepath=$HOME/src/repository
mails=(antons@coins.exchange)

declare -A envs
envs["tests"]="$HOME/tests/tests_crm_bo"

for e in ${!envs[@]}; do
    find . -name "./tests/tests_crm_bo/*/*test.py" -print | while read f; do
        echo "$f"
        ###
        python -m coverage run "$f"
        ###for m in ${mails[@]}; do
	echo "File $filepath"
        echo "Sending report message to $m with env $e"
        mail -s "Report Postman. ENV: $e" $m < $filepath
    done
done
