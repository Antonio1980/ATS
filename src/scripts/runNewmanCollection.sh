#!/bin/bash

filepath=$HOME/reportAPI
mails=(antons@coins.exchange)

declare -A envs
envs["prod"]="$HOME/src/repository/DX.postman_environment.json"
col = "$HOME/src/repository/ForgotPasswordTests.postman_collection.json"

for e in ${!envs[@]}; do
    echo Running environment ${envs[$e]}
    'C:\nodejs' 'C:\nodejs\node_modules\newman\bin\newman.js' run col -e ${envs[$e]} | tee $filepath
    for m in ${mails[@]}; do
	echo "File $filepath"
        echo "Sending report message to $m with env $e"
        mail -s "Report Postman. ENV: $e" $m < $filepath
    done
done
