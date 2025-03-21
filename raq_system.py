import requests
from AI_Models import Google_Custom_Search_Engine
from Ai_API_Key import Custom_Search_API
API_KEY = Custom_Search_API  # جایگزین با کلید API شما
SEARCH_ENGINE_ID = Google_Custom_Search_Engine  # جایگزین با Search Engine ID شما

def google_search(query, num_results=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": num_results,
        "start": 1  # شروع از اولین نتیجه
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    links = [item["link"] for item in data.get("items", [])]
    return links
