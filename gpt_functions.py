import os
import json
import openai
import pprint
from dotenv import load_dotenv
from google_search import *
import tiktoken

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')


def get_query(input_query):

    query_message = {
        "role": 'system',
        # multi-line string
        "content": """You are a subsystem of a larger
        system that is used to search the web. Your role is to
        return the most relevant and complete query that can be used to browse
        the web based on the input query. STRICTLY return the query as a dictionary
        with the following key: optimized_search_query.    
        """
    }

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.0,
        messages=[query_message, {"role": 'user', "content": input_query}],
    )

    content = response['choices'][0]['message']['content']
    # turn content string into json
    content = json.loads(content)

    return content


def decide_leads(links, query):

    sys_message = {
        'role': 'system',
        'content': """
        Your task is to evaluate the provided links and determine which ones 
        are the most suitable for finding information related to the given query. 
        Return the most most suitable links as a JSON object with the key "link", 
        Just a string JSON no backticks.
        """
    }

    user_message = {
        'role': 'user',
        'content': f"The query is {query}. The links are ```{links}```."
    }

    messages = [sys_message, user_message]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.0,
        messages=messages,
    )

    content = response['choices'][0]['message']['content']
    content = json.loads(content)
    return content
# pprint.pprint(get_query('what is apple latest product that is released?'))


def summarize(query, webpage):

    sys_message = {
        'role': 'system',
        'content': """
        Your task is to summarize the webpage content based on the query asked by the user. 
        Make sure the answer returned isn't needlessly long and make sure it is well explained and not copied.
        Strictly return the summary as a JSON object with the following key: 
        'summary' in double quotes.
        RETURN A JSON OBJECT WITH THE KEY SUMMARY
        If the answer can not be deterined from the provided webpage, return the value "N/A" as the summary.
        """
    }

    enc_webpage = encoding.encode(webpage)
    #truncate the encoding to 2048 tokens
    enc_webpage = enc_webpage[:2048]
    webpage = encoding.decode(enc_webpage)

    user_message = {
        'role': 'user',
        'content': f"The query is {query}. The webpage is ```{webpage}```."
    }

    messages = [sys_message, user_message]

    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        temperature=0.0,
        messages=messages,
    )

    content = response['choices'][0]['message']['content']
    print(content)
    content = json.loads(content)
    return content


# test_links = {"Apple Event: what's happened in 2023 and what could be next - TechRadar": 'https://www.techradar.com/news/new-apple-event',
#  'Apple shows off MacBooks with M3 chip at Scary Fast event - Yahoo Finance': 'https://finance.yahoo.com/video/apple-shows-off-macbooks-m3-140203045.html',
#  'Apple unveils new MacBook Pro featuring M3 chips': 'https://www.apple.com/newsroom/2023/10/apple-unveils-new-macbook-pro-featuring-m3-chips/',
#  "Apple's 'Scary Fast' Mac event: all the news from Apple's online keynote - The Verge": 'https://www.theverge.com/2023/10/30/23933672/apple-event-mac-october-news-updates-products-scary-fast',
#  'Apple: News, Reviews, Guides, and More - PCMag': 'https://www.pcmag.com/series/apple',
#  'Every new Apple product coming in 2024 - Macworld': 'https://www.macworld.com/article/671090/new-apple-products.html',
#  'The new MacBook Pro | Apple - YouTube': 'https://youtube.com/watch?v=0pg_Y41waaE',
#  'Upcoming Apple Products Guide: Everything We Expect to See in 2023 and Beyond': 'https://www.macrumors.com/guide/upcoming-apple-products/'}

# pprint.pprint(decide_leads(test_links, 'Apple latest product released'))

# pprint.pprint(summarize('what is apple latest product that is released?', """The iPhone 15 Pro and iPhone 15 Pro Max were this year's headlining act, with new and improved form factors, updated processors, and the latest advancements in the iPhone camera.

# The biggest change, at least on the surface, is the slimmer and lighter design, which has new contoured edges, Grade 5 Titanium, and the thinnest borders ever on an iPhone.

# Also: iPhone 15 Pro hands-on: I found a lot of reasons to upgrade and one to wait until next year

# The iPhone 15 Pro features the fastest mobile CPU -- A17 Pro. The new CPU can run up to 10% faster than the A16 Bionic chip in last year's iPhone 14 Pro. Compared to Apple's previous iterations, the neural engine is up to two times faster, and the pro-class GPU is up to 20 times faster, optimizing overall smartphone performance.

# As for the cameras, the Pro variants feature a 48MP main camera, which allows users to switch between the 24mm, 28mm, and 35mm focal lengths and supports 48MP HEIF images with up to four times the resolution. The Pro Max also features a 5X telephoto lens, the longest optical zoom ever on iPhone.

# Like on the iPhone 15 and iPhone 15 Plus, Portrait Mode now runs in the background, so the iPhone can measure the depth information of a photo's subject and later give users the ability to adjust the bokeh effect. The quality of photos in low light will also improve, with a night mode that provides sharper detail and more vivid colors.

# Also: 4 key features the iPhone 15 Pro is still missing

# Besides the cameras, another major selling point is the Action Button, which replaces the traditional alert slider. The Action Button will function as a ring and silent button by default but can be personalized to be a mappable quick key for turning on the camera app, flashlight, Siri, Shortcuts, and more.

# In terms of safety, the phones feature Crash Detection, Emergency SOS via satellite, and a new Roadside Assistant that allows customers to comment to AAA when experiencing car troubles.

# Also: Apple iPhone 15 Pro mutes side switch for multifunctional Action button

# With the EU imposing a law for electronics makers to adopt USB-C by 2024, the new iPhones finally support charging and data transferring via USB-C, becoming Apple's latest major product to make the switch to the more universal power format.

# The phones are available for preorder now in black titanium, white titanium, blue titanium, and natural titanium finishes. The iPhone 15 Pro starts at $999, and the iPhone 15 Pro Max starts at $1,199."""))
