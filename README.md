
# ChatGPT & Google Search Integration Project

## Overview

This project aims to enhance the capabilities of ChatGPT by integrating it with Google Search. By doing so, ChatGPT can leverage real-time search results to provide up-to-date and relevant responses to user queries.

## Components

The project consists of several Python scripts that work together to perform web searches and process the results:

- `google_search.py`: Interfaces with the Google Search API to fetch search results.
- `gpt_functions.py`: Contains functions to optimize search queries using ChatGPT and to decide which search results are most relevant.
- `google_GPT_class.py`: Defines a class that combines the functionalities of the above scripts to perform the entire search and response generation process.

## Installation

1. Install the required Python packages, this can be done using this `requirements.txt` file:

```bash
pip install -r requirements.txt
```

2. Set up your environment variables:

```env
OPENAI_API_KEY='your-openai-api-key'
SERPER_API_KEY='your-serp-api-key'
```

## Usage

Create an instance of the `GoogleGPT` class and call the `search` method with a query:

```python
from google_GPT_class import GoogleGPT

gGPT = GoogleGPT()
results = gGPT.search('Latest technology trends in AI')
```

The `search` method performs the following steps:

1. Takes a user's input query.
2. Optimizes the query for search.
3. Fetches search results from Google.
4. Uses ChatGPT to select the most relevant search result.
5. Extracts content from the selected search result.
6. Summarizes the content related to the original query.
7. Returns the summary.

## Functions

### `google_search.py`

- `search_results(payload)`: Posts a query to the Google Search API and returns search results.
- `extract_webpage_content_efficient(url)`: Extracts and returns the main text content from a webpage URL.

### `gpt_functions.py`

- `decide_leads(links, query)`: Determines which of the provided search result links are most relevant to the query.

### `google_GPT_class.py`

- `search(query)`: Orchestrates the entire process of searching and processing the results to answer the user's query.

## Conclusion

This integration allows ChatGPT to access and utilize real-time information from the web, greatly expanding its knowledge base and relevance.
