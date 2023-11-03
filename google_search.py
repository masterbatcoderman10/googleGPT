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



def search_results(payload):
    """
    Fetches search results from a Google Search API.

    This function sends a POST request to the Google Search API with a given payload. 
    It then parses the response and extracts the title and link of each organic search result.

    Args:
        payload (dict): The payload to send in the POST request. This should contain the search parameters.

    Returns:
        dict: A dictionary where the keys are the titles of the search results and the values are the corresponding links.
    """
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': serp_api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    links = {org['title']: org['link'] for org in data['organic']}
    return links


# pprint.pprint(search_results('Apple latest product'))


# def extract_webpage_content(url):
#     try:
#         # Make an HTTP request to the webpage
#         response = requests.get(url)
#         response.raise_for_status()  # Check if the request was successful
#     except requests.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")
#         return None
#     except Exception as err:
#         print(f"An error occurred: {err}")
#         return None

#     # Parse the webpage content with Beautiful Soup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Get the text content from the webpage
#     text_content = soup.get_text(separator='\n', strip=True)

#     return text_content

def extract_webpage_content_efficient(url):
    """
    Extracts the main content from a webpage.

    This function uses the Newspaper3k library to download and parse the webpage. 
    It then extracts the main text content from the parsed webpage.

    Args:
        url (str): The URL of the webpage to extract content from.

    Returns:
        str: The main text content of the webpage.
    """
    article = Article(url)
    article.download()
    article.parse()

    main_text = article.text
    return main_text


# page_content =extract_webpage_content_efficient(
#     "https://www.zdnet.com/article/every-product-apple-announced-this-week-iphone-15-pro-apple-watch-series-9-airpods/")

# encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
# print(len(encoding.encode(page_content)))

# print(page_content)
