import csv, sys

class Config:

    def __init__(self):
        self.path = sys.path[1] + "\\TestData\\"
        self.filename = 'tests_data.csv'
        self.username = ""
        self.password = ""
        self.url = ""
        self.drivers = ""
        self.data = []


    def setAttributes(self):
        with open(path+filename, 'r') as f:
            mycsv = csv.reader(f)
            mycsv = list(mycsv)
            self.username = mycsv[0][1]
            self.password = mycsv[1][1]
            self.url = mycsv[2][1]
            self.drivers = mycsv[3][1]
            self.data = [username,password,url,drivers]
        return self





