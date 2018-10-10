#!/usr/bin/env bash

timestamp=$(date +"%s")
collection=/var/www/myapp/tests/collection.json
env=/var/www/myapp/tests/envfile.json

# create separate outfile for each run
outfile=/var/www/myapp/tests/outfile-${timestamp}.json

# redirect all output to /dev/null
newman -c ${collection} -c ${env} -o ${outfile} > /dev/null2>&1