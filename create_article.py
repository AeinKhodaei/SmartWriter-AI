from openai import OpenAI
from AI_Models import Google_Custom_Search_Engine , openrouter_modle
from Ai_API_Key import Custom_Search_API , openrouter_API
from raq_system import raq_system

def CreateArticleText(title , word , raq_data):
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
            "text": """یک مقاله‌ی جامع و اصولی به زبان فارسی بنویس. **عنوان مقاله باید دقیقاً همان باشد که ارائه شده است**، اما می‌توانی **کلمات کلیدی مرتبط** را برای بهبود سئو و پوشش بهتر موضوع اضافه کنی.  
مقاله باید ساختاری منظم، نگارشی حرفه‌ای و اطلاعات دقیق داشته باشد. **از مقالات داده‌شده برای تولید محتوا استفاده کن** و در صورت نیاز، اطلاعات را ترکیب و بازنویسی کن تا متنی منحصربه‌فرد و روان ایجاد شود.  
مقاله نباید از محوریت اصلی موضوع خارج شود و باید **کاربر را مستقیماً و به‌سرعت به پاسخ موردنظرش برساند**.  
در صورت نیاز، برای نمایش بهتر داده‌ها یا مقایسه‌ها، از **جداول** استفاده کن.  
"""
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f""""
            عنوان : {title}
            کلمات کلیدی : {word}
            اطلاعات استخراج شده از دگرسایت ها : 
            {raq_data}"""
            }
        ]
        }
    ]
    )
    return completion.choices[0].message.content


