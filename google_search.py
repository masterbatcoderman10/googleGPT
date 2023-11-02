import os
import http.client
import dotevn
import json
import pprint
dotevn.load_dotenv()

serp_api_key = os.getenv("SERPER_API_KEY")