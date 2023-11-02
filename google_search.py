import os
import http.client
import dotenv
import json
import pprint
import requests
from bs4 import BeautifulSoup
import tiktoken
from newspaper import Article

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

# pprint.pprint(search_results('Apple latest product'))


def extract_webpage_content(url):
    try:
        # Make an HTTP request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    # Parse the webpage content with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the text content from the webpage
    text_content = soup.get_text(separator='\n', strip=True)

    return text_content

def extract_webpage_content_efficient(url):

    article = Article(url)
    article.download()
    article.parse()

    main_text = article.text
    return main_text


page_content =extract_webpage_content_efficient(
    "https://www.zdnet.com/article/every-product-apple-announced-this-week-iphone-15-pro-apple-watch-series-9-airpods/")

# encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
# print(len(encoding.encode(page_content)))

print(len(page_content))
