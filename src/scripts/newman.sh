#!/bin/bash

filepath=$HOME/reportAPI
mails=(antons@coins.exchange)

declare -A envs
envs["prod"]="$HOME/src/repository/files/QA.postman_environment.json"
col = "$HOME/src/repository/files/RegistrationWithCustomEmail.postman_collection.json"

for e in ${!envs[@]}; do
    echo Running environment ${envs[$e]}
    'newman' run col -e ${envs[$e]} | tee $filepath
    for m in ${mails[@]}; do
	echo "File $filepath"
        echo "Sending report message to $m with env $e"
        mail -s "Report Postman. ENV: $e" $m < $filepath
    done
done
