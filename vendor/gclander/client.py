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
        credentials = credentials.with_subject('info@propstart.com.au')
        service_account_email = "info@propstart.com.au"
        

        self.service = build('calendar', 'v3', credentials=credentials)
    # start_datetime.isoformat()
    def gc_event(self, attendee, start_date):
        
        service = self.service
        start_datetime = datetime.datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                calendarId="info@propstart.com.au",
                body={
                    "summary": "Book A Call",
                    "description": "Strategy Call",
                    "start": {"dateTime": start_date.isoformat()},
                    "end": {
                        "dateTime": (start_date + timedelta(minutes=30)).isoformat()
                    },
                    "attendees": [{"email":attendee, }],
                    'sendNotifications': True,
                },
            )
            .execute()
        )
        print(event)