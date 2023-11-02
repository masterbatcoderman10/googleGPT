import os
import json
import openai
import pprint
from dotenv import load_dotenv
from google_search import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_query(input_query):

    query_message = {
        "role": 'system',
        # multi-line string
        "content": """You are a subsystem of a larger
        system that is used to search the web. Your role is to
        return the most relevant query that can be used to browse
        the web based on the input query. STRICTLY return the query as a dictionary
        with the following key: optimized_search_query.    
        """
    }

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=[query_message, {"role": 'user', "content": input_query}],
    )

    content = response['choices'][0]['message']['content']
    # turn content string into json
    content = json.loads(content)

    return content


def decide_leads(links, query):
    """
    This function uses the openai chat to decide which of the links is the most appropriate for a given query
    """

    sys_message = {
        'role': 'system',
        'content': 'Your job is to decide which of the provided links is the most suitable to find information relating to the the provided query. Strictly return the most suitable link as a dictionary with the following key: link in double quotes.'
    }

    user_message = {
        'role': 'user',
        'content': f"The query is {query}. The links are ```{links}```."
    }

    messages = [sys_message, user_message]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.5,
        messages=messages,
    )

    content = response['choices'][0]['message']['content']
    content = json.loads(content)
    return content
# pprint.pprint(get_query('what is apple latest product that is released?'))


test_links = {'Apple Accessories for Apple Watch, iPhone, iPad, and Mac': 'https://www.apple.com/shop/accessories/all',
              'Apple Store Online': 'https://www.apple.com/store',
              'Every new Apple product coming in 2024 - Macworld': 'https://www.macworld.com/article/671090/new-apple-products.html',
              'Every product Apple announced this week: iPhone 15 Pro, Apple Watch Series 9, AirPods': 'https://www.zdnet.com/article/every-product-apple-announced-this-week-iphone-15-pro-apple-watch-series-9-airpods/',
              'The iPhone 15 and Other Apple Products We Still Expect in 2023 - CNET': 'https://www.cnet.com/tech/mobile/iphone-15-and-other-apple-products-we-still-expect-in-2023/',
              'The new MacBook Pro | Apple - YouTube': 'https://youtube.com/watch?v=0pg_Y41waaE',
              'Timeline of Apple Inc. products - Wikipedia': 'https://en.wikipedia.org/wiki/Timeline_of_Apple_Inc._products',
              "What's New - All Accessories - Apple": 'https://www.apple.com/shop/accessories/all/whats-new'}

pprint.pprint(decide_leads(test_links, 'Apple latest product released'))

