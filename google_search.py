import os
import http.client
import dotenv
import json
import pprint
dotenv.load_dotenv()

serp_api_key = os.getenv("SERPER_API_KEY")


def search_results(query):

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "num": 10,
    })
    headers = {
        'X-API-KEY': serp_api_key,
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # load data into json
    data = json.loads(data)
    # pretty print json
    links = {org['title']: org['link'] for org in data['organic']}

    return links

pprint.pprint(search_results('Apple latest product'))
