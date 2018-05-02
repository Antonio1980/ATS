# !/usr/bin/env python
# -*- coding: utf8 -*-

import csv


def get_csv_data(data_file):
    rows = []
    with open(str(data_file), "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)

    return rows


def get_csv_by_value(data_file):
    with open(data_file, 'r') as f:
        mycsv = csv.reader(f)
        next(mycsv, None)
        mycsv = list(mycsv)
        username = mycsv[0][0]
        password = mycsv[0][1]
