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
    def gc_event(self, attendee, start_date, phone=None):
        
        service = self.service
        start_datetime = datetime.datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                calendarId="info@propstart.com.au",
                body={
                    "summary": f"Book A Call {phone}",
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

    def available_times(self):
        from datetime import datetime, timedelta
        today = datetime.now()

        end_date = today + timedelta(days=30)  
        start_time = datetime(today.year, today.month, today.day, 8, 0, 0)
        end_time = datetime(end_date.year, end_date.month, end_date.day, 18, 0, 0)
        
        service = self.service
        events_result = service.events().list(
            calendarId="info@propstart.com.au",
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        print("Available Times", events)

    