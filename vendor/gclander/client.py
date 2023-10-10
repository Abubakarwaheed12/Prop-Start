from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from datetime import timedelta
import pytz




class GoogleAPIClient:

    def __init__(self):

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        credentials = service_account.Credentials.from_service_account_file(
            './gclient_secret.json',
            scopes=SCOPES,
        )
        credentials = credentials.with_subject('noreply@propstart.com.au')
        service_account_email = "noreply@propstart.com.au"
        

        self.service = build('calendar', 'v3', credentials=credentials)
    # start_datetime.isoformat()
    def gc_event(self, title, description, attendee):
        
        service = self.service
        start_datetime = datetime.datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                calendarId="noreply@propstart.com.au",
                body={
                    "summary": "Book A Call",
                    "description": "Book A Call Meeting",
                    "start": {"dateTime": start_datetime.isoformat()},
                    "end": {
                        "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                    },
                    "attendees": [{"email":"abubakarjutt6346527@gmail.com", }],
                    'sendNotifications': True,
                },
            )
            .execute()
        )
        print(event)