from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import timedelta
import pytz

SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    filename="./gclient_secret.json", scopes=SCOPES
)

def build_service():
    service = build("calendar", "v3", credentials=credentials)
    return service


class GoogleAPIClient:

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        # Load the service account credentials with delegation
        credentials = service_account.Credentials.from_service_account_file(
            './gclient_secret.json',
            scopes=SCOPES,
        )
        credentials = credentials.with_subject('propstart@propstart.iam.gserviceaccount.com')
        service_account_email = "abubakarjutt6346527@gmail.com"
        
        # Create the Calendar API client

        self.service = build('calendar', 'v3', credentials=credentials)
    # start_datetime.isoformat()

    def gc_event(self, title, description, attendee):
        service = build_service()
        # event = {
        #     'summary': title,
        #     'description': description,
        #     'start': {'dateTime': '2023-10-06T14:00:00', 'timeZone': 'UTC'},
        #     'end': {'dateTime': '2023-10-06T14:30:00', 'timeZone': 'UTC'},
        #     'attendees': [{'email': 'noreply@propstart.com.au'}] + [{'email': attendee}],
        #     'reminders': {
        #         'useDefault': False,
        #         'overrides': [
        #             {'method': 'email', 'minutes': 30},  # Send an email notification 30 minutes before the event
        #         ],
        #     },
        # }
        # # Insert the event into the calendar
        # created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        # print('created_event', created_event)

        # return created_event
        start_datetime = datetime.datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                calendarId="0a45566e61f1be80bc686325639071dabc79547ac76358b49576b59c0ccc4be8@group.calendar.google.com",
                body={
                    "summary": "Book Call",
                    "description": "Book A Call Event",
                    "start": {"dateTime": start_datetime.isoformat()},
                    "end": {
                        "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                    },
                    "attendees": [{"email":"hamidnwl123@gmail.com",  "responseStatus": "needsAction"}],
                },
            )
            .execute()
        )
        print(event)