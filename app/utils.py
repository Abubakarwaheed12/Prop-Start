# All The Lead Types
# New course
# Strategy session
# Attempt to schedule
# Coaching session
# Property presentation
# New strategy request
# New referral
# New course
# New strategy request
from vendor.hubspot.client import APIClient as HubspotAPIClient
playload = {
    "fname" : "abubakar",
    "lname" : "waheed",
    "email" : "abubakarjutt6346527@gmail.com",
    "phone" : "03416346527",
    "lead_status" : "Strategy session",
}

def send_to_hubspot(*args, **kwargs):
    api = HubspotAPIClient()
    c_id =api.create_or_update_contact({
        "firstname" : kwargs.get("fname", "dummy"),
        "lastname": kwargs.get("lname", "dummy"), 
        "email": kwargs.get("email", "exap@gmauil.com"),
        "phone": kwargs.get("phone", "03416346527"),
        "hs_lead_status": kwargs.get("lead_status", "Strategy session"),
    })