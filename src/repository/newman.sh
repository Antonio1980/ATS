#!/usr/bin/env bash

timestamp=$(date +"%s")
collection=tests_sources/test_data/services_collection.json
env=tests_sources/test_data/services_environment.json

# mail settings
RCVR="antons@coins.exchange"
SUBJ="Test Failed"

# create separate outfile for each run
outfile=tests_sources/test_data/logs/outfile-${timestamp}.json

# capture newman STDERR status
command="$(newman -c ${collection} -e ${env} -o ${outfile} 2>&1 > /dev/null)"

# send mail if STDERR is not 0
if [ "$?" -ne "0" ]; then
	mail ${RCVR} -s "$SUBJ"
fi