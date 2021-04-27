from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import pandas as pd

expirations = pd.read_csv('expeirations.csv', delimiter=',')

SCOPES = 'https://www.googleapis.com/auth/calendar'

store = file.Storage('token.json')

creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3' , http=creds.authorize(Http()))

calendar_list_entry = service.calendarList().get(calendarId='primary').execute()

if calendar_list_entry['accessRole']:
	
	event = {
		'summary': "Azerbaijan-Baku_ARIS 15 Licsnses Expires",
		'location': snip,
		'description':snip ,
		'start': {
			'dateTime': 2021-03-31,
			'timeZone': 'America/Denver',
		},
		'end': {
			'dateTime': 2021-03-31,
			'timeZone': 'America/Denver',
		},
	}

		event = service.events().insert(calendarId='primary', body=event).exicute()		
		print(f"The event has been created! View it at {event.get('htmlLink')}!")