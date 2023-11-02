import os
import json
import openai
import pprint
from dotenv import load_dotenv

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


pprint.pprint(get_query('apples latest product'))