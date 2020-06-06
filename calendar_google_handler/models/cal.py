import datetime
import pickle
import os.path
import sys
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print('please install the google api tools by executing:' )
    print('pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib')
    sys.exit()

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDARS = [
    '1 Öffentliche Veranstaltungen',
    '2 Interne Notizen',
    '3 Privatvermietungen',
    '4 Vorreservation',
    '6 BT Admin',
    '7 Tagesschule',
]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    # here we only look at the primary event
    # it has the setting: 'primary': True,
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        
    # now just list our events
    calendars = service.calendarList().list().execute()
    for calendar in calendars['items']:
        if calendar.get('summary') in CALENDARS:
            print('id:%(id)s, summary:%(summary)s' % calendar)
            events_result = service.events().list(calendarId=calendar['id'], timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            print(events)
    


if __name__ == '__main__':
    main()