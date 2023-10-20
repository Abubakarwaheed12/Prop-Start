import requests
from django.conf import settings


class APIClient:
    base_url = 'https://api.hubapi.com'
    API_KEY = settings.HUBSPOT_API_KEY

    def get(self, path, params={}):
        return requests.get(
            f'{self.base_url}{path}',
            headers={
                'Authorization': f'Bearer {self.API_KEY}',
            },
            params=params
        )

    def delete(self, path):
        return requests.delete(
            f'{self.base_url}{path}',
            headers={
                'Authorization': f'Bearer {self.API_KEY}',
            },
        )

    def post(self, path, payload):
        return requests.post(
            f'{self.base_url}{path}',
            headers={
                'Authorization': f'Bearer {self.API_KEY}',
            },
            json=payload
        )

    def put(self, path, payload, extra_params={}):
        return requests.put(
            f'{self.base_url}{path}',
            headers={
                'Authorization': f'Bearer {self.API_KEY}',
            },
            params=extra_params,
            json=payload
        )

    def create_or_update_contact(self, customer):
        assert 'email' in customer, "Email is required to create / update a hubspot contact."

        request = {
            'properties': []
        }
        desired_fields = {
            'email', 'company', 'phone', 'website', 'budget', 'category', 'company_size', 'goals',
            'ga_source', 'ga_medium', 'ga_content', 'ga_term', 'ga_campaign', 'landing_page', 'conversion_page',
            'ruid', 'brand_source', 'hs_lead_status', 'lead_source', 'lead_source_details', 'firstname',
            'lastname', 'form_name'
        }

        for k, v in customer.items():
            if k not in desired_fields:
                print('Skipping field/property because its not in our list: %s', k)
                continue
            request['properties'].append({
                'property': k,
                'value': v,
            })

        r = self.post(
            f"/contacts/v1/contact/createOrUpdate/email/{customer['email']}/",
            payload=request,
        )
        if r.status_code == 400:
            print(r.json())
            r.raise_for_status()
        elif r.status_code == 409:
            print('Lead already existed with email: %s', customer['email'])
            contact_id = r.json()['identityProfile']['vid']
        else:
            contact_id = r.json()['vid']

        return contact_id

    def create_contact_with_company(self, contact_data, company_id) -> dict:
        if not company_id or not contact_data:
            return {}
        path = '/crm/v3/objects/contacts'
        payload = {
            "properties": {
                'associatedcompanyid': company_id,
                **contact_data,
            }
        }
        response = self.post(path, payload)
        return response.json()

    def get_all_contacts(self, offset=0):
        path = '/contacts/v1/lists/all/contacts/all'
        params = {
            'count': 100,
            'vidOffset': offset,
            'property': 'website',
            'formSubmissionMode': 'all',
        }
        response = self.get(path, params=params)
        return response

    def get_contact(self, contact_id) -> dict:
        if not contact_id:
            return {}
        path = f'/contacts/v1/contact/vid/{contact_id}/profile'
        response = self.get(path)
        return response.json()

    def get_contact_with_email(self, email: str) -> dict:
        if not email.strip():
            return {}
        path = f'/contacts/v1/contact/email/{email}/profile'
        response = self.get(path)
        return response.json()

    def delete_contact(self, contact_id) -> dict:
        if not contact_id:
            return {}
        path = f'/contacts/v1/contact/vid/{contact_id}'
        response = self.delete(path)
        return response.json()


    def create_deal_with_contact_id(self):
        path = '/crm/v3/objects/deals'
         
        payload = {
            "properties": {
                "amount": "1500.00",
                "closedate": "2023-12-07T16:50:06.678Z",
                "dealname": "Strategy Call",
                "pipeline": "default",
                "dealstage": "contractsent",
                "hubspot_owner_id": "552621387"
            },
           
            "associations": [
                    {
                     "to": {
                        "id": 651
                      },
                      "types": [
                        {
                          "associationCategory": "HUBSPOT_DEFINED",
                          "associationTypeId": 3
                        } ]
                    }, ]
        }

        


        response = self.post(path, payload)
        print("response", response.json())
        if response.status_code == 201:
            r = response.json()
            deal_id = r['id']
            return response.json()
        else:
            return {
                'error': f'Error: {response.status_code} - {response.text}'
            }

        