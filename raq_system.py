import requests
from bs4 import BeautifulSoup
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

def get_article_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج تگ‌های مورد نظر
        tags = ['h1', 'h2', 'h3', 'p' , 'a']
        extracted_content = []
        
        for tag in tags:
            for element in soup.find_all(tag):
                text = element.get_text(separator=' ', strip=True)
                if text:
                    extracted_content.append(f"<{tag}> {text}")
        
        return '\n'.join(extracted_content) if extracted_content else "محتوایی یافت نشد."
    
    except requests.exceptions.RequestException as e:
        return f"خطا در دریافت داده: {e}"