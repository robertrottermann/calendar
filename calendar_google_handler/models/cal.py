import datetime
import pickle
import os.path
import sys
import json
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

json_cred = {"installed":{"client_id":"694254662460-19semoouffjvjtb9cpn3eua5ueb8vl4s.apps.googleusercontent.com","project_id":"quickstart-1591465275497","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"v7Eq9g5nRZI6AuK5XA765j94","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}


# check how odoo is handling the storing of google credentials
# in the google calendar sync
client_secrets = os.path.join(os.path.dirname(__file__), "client_secrets.json")
pickle_file = os.path.join(os.path.dirname(__file__), 'token.pickle')
def check_credentials_exist():
    """ get file name with credentials
        if it does not exist, create it

        We should handle that in an "odoo" way.
        Check how the google_calendar module handles this
    """
    # Name of a file containing the OAuth 2.0 information for this
    # application, including client_id and client_secret, which are found
    # on the API Access tab on the Google APIs
    # Console <http://code.google.com/apis/console>.
    if not os.path.exists(client_secrets):
        with open(client_secrets, 'w') as f:
            f.write(json.dumps(json_cred))
            f.close()

def get_google_service():
    """ log in to google
        Use a file with credentials. If this file does not exist, create it

    Returns:
        service: a google service channal, trough which we can communicate
                 with google calendars
    """
    creds = None
    check_credentials_exist()
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events_for_summary(summary):
    """get all events defined for a calendar

    Args:
        summary (string): the summary field used as a key to find the calendar

    Returns:
        list of dictionaries: all upcoming events found for the google calendar
    """
    service = get_google_service()
    calendars = service.calendarList().list().execute()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    for calendar in calendars['items']:
        if calendar.get('summary') == summary:
            print('id:%(id)s, summary:%(summary)s' % calendar)
            events_result = service.events().list(calendarId=calendar['id'], timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            return events

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    service = get_google_service()

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
    for summary in CALENDARS:
        get_events_for_summary(summary)

if __name__ == '__main__':
    main()