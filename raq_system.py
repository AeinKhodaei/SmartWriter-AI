import requests
from bs4 import BeautifulSoup
from AI_Models import Google_Custom_Search_Engine , openrouter_modle
from Ai_API_Key import Custom_Search_API , openrouter_API
from openai import OpenAI
API_KEY = Custom_Search_API  # جایگزین با کلید API شما
SEARCH_ENGINE_ID = Google_Custom_Search_Engine 
 # جایگزین با Search Engine ID شما
def SuggestSearchTitles(title , words):
    client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= openrouter_API,
    )

    completion = client.chat.completions.create(
    model= openrouter_modle,
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": """شما یک هوش مصنوعی پیشرفته برای پیشنهاد عبارات جستجو هستید. بر اساس **عنوان مقاله** و **کلمات کلیدی** داده‌شده، **۴ عبارت جستجو** پیشنهاد دهید:  
- ۲ عبارت برای جستجو در منابع انگلیسی  
- ۲ عبارت برای جستجو در منابع فارسی  
- فقط عبارات جستجو را نمایش دهید و هیچ متن اضافی ننویسید.  
- هر عبارت را در یک خط بنویس.  

### ورودی نمونه:  
عنوان مقاله: **تأثیر هوش مصنوعی در بازاریابی دیجیتال**  
کلمات کلیدی: **هوش مصنوعی، بازاریابی دیجیتال، تبلیغات هوشمند، تحلیل داده**  

### خروجی مورد انتظار:  
AI impact on digital marketing  
Best AI tools for online advertising  
تأثیر هوش مصنوعی بر بازاریابی دیجیتال  
بهترین ابزارهای هوش مصنوعی برای تبلیغات  
"""
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"""
عنوان : {title}
کلمات کلیدی : {words}"""
            }
        ]
        }
    ]
    )
    return completion.choices[0].message.content

def google_search(query, num_results=2):
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

def HTMLTAGStoArticle(text):
    client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= openrouter_API,
    )

    completion = client.chat.completions.create(
    model= openrouter_modle,
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": """You are an AI writer tasked with generating a complete and readable article from structured data. The input text includes headings, paragraphs, and categories. Your job is to:

Reconstruct the text into a well-organized and readable article.
Remove unrelated, redundant, or unnecessary sections. This includes information such as author names, dates, comments, sign-up requests, advertisements, and any text unrelated to the main topic.
Maintain the original structure of the article without altering its core content.
Use the provided headings to create the article’s sections and place the paragraphs appropriately.
Ensure the final article is natural, readable, and well-formatted for publication.
If the article contains comparisons, you may use tables when necessary to present the information clearly.
The output should not be in HTML tags and must be provided as plain text only.
Expected Output:
A complete, structured, and readable article with the original content intact but without unnecessary and unrelated sections."""
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f""""
            You will receive 1 structured articles. Your task is to reorganize them into a clear and readable format, remove any irrelevant content, and maintain the original structure of the article.
            text [{text}]"""
            }
        ]
        }
    ]
    )
    return completion.choices[0].message.content
def raq_system(title , words):
    texts = ""
    article = ""
    SearchTitles = SuggestSearchTitles(title , words)
    print("Geting SearchTitles ....")

    SearchTitles_list = SearchTitles.split("\n")
    for i in SearchTitles_list:
        article_links = google_search(i)
        print("Searching for title ....")
        for i in article_links:
            print("Producing sub-articles ....")
            article_text = get_article_content(i)
            article = article + HTMLTAGStoArticle(article_text)+"\n"+"-------------------------------------------------------------------------"+"\n"
    return article

