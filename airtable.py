import requests

AIRTABLE_BASEID='appAfgNCoslMU4ehB'
AIRTABLE_TOKEN='keyVMBAulTbdEjLdo'
AIRTABLE_NAME='testbase_1'

endpoint=f'https://api.airtable.com/v0/{AIRTABLE_BASEID}/{AIRTABLE_NAME}'


# def add_to_airtable(email=None, name=""):
#     if email is None:
#         return
#     headers = {
#         "Authorization": f"Bearer {AIRTABLE_TOKEN}",
#         "Content-Type": "application/json"
#     }
#
#     data = {
#         "records": [
#             {
#                 "fields": {
#                 "Name": name,
#                 "Email": email
#                 }
#             }
#         ]
#     }
#     r = requests.get(endpoint, json=data, headers=headers)
#     print(r.json())

# add_to_airtable('abc123@gmail.com', name='devika')

def get_names(Name):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASEID}/{AIRTABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    records = []
    params = {
        "fields": ["Name", "time"],
        "filterByFormula": "NOT % 28 % 7 BName % 7 D % 20 % 3 D % 20 % 27 % 27 % 29"
    }


    res = requests.request("Get", url, headers=headers, params=params)
    print(res.json())

get_names(Name='')



