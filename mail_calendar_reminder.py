from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import MySQLdb
import sys
import calendar
import smtplib
from datetime import date
from email.mime.text import MIMEText

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
d3 = date.today()
d4 = d3.strftime("%Y-%m-%d")
print(d4)
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
def main():
    credentials = get_credentials()
    http1 = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http1)
    event = {
      'summary': 'Paying Insurance Amount ',
      'location': 'India',
      'description': 'The insurance details have been mailed to your e-mail address',
      'start': {
        'date': d4,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'date': d4,
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'attendees_email_id'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))
d = date.today()
d1 = str(d.strftime("%d.%m.%Y"))
def modify(d1) : 
	index = 0
	s = ''
	for i in d1 :
		if(index < 8) : 
			s = s + i
		else :
			s = s + 'X'
		index = index + 1
	return s
que = modify(d1)
s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
s.login("mail_id","password")
message = " Time to pay the insurance "
connection = MySQLdb.connect (host = "localhost", user ="mysql_user",passwd = "mysql_password",db = "db_name")
cursor = connection.cursor ()
cursor.execute ('SELECT Number, Amount from insurancetable where Date = %s',(que,))
data = cursor.fetchall ()
flag = 0;
for row in data:
	message1 = str(row)
	msg = MIMEText('The insurance number and amount is mentioned in the parenthesis.'+message1)
	msg['Subject'] = 'Insurance Payment detail'
	#message2 = "The insurance number and amount is as :" + message1  
	s.sendmail("sender","recipient",msg.as_string())
	if __name__ == '__main__':
		main()
s.quit()
cursor.close ()
connection.close ()
sys.exit ()