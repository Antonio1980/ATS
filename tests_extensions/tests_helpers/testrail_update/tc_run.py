from testrail import *
import configparser
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('run', help='Testrail TestRun number',
                    type=int ) # run - parameter for setting the number of Test Ran in which TC start. TC number - constant

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('logintr.ini', encoding='utf-8-sig') # logintr.ini - txt file with info

user=config.get('testrail', 'user')
password=config.get('testrail','password')
server=config.get('testrail', 'server')

client=APIClient(server)
client.user = user
client.password = password

case = client.send_get('get_case/41')

result = client.send_post(
	'add_result_for_case/'+str(args.run)+'/41',
	{ 'status_id': 1, 'comment': 'This test worked2!' }
)


print(case)
print ('******************************')
print ('******************************')
print(result)