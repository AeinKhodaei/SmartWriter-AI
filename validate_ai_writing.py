import openai
from Ai_API_Key import OPENAI_API , validate_ai_writing_Modle
def chat_with_gpt(title):
    client = openai.OpenAI(api_key= OPENAI_API)

    response = client.chat.completions.create(
        model= validate_ai_writing_Modle,
        messages=[
            {"role": "system", "content": """You are an AI model. Check whether you can generate a complete and informative article based on the given title.  

### Conditions for Evaluation:  
1. **Availability of Information:**  
   - If you have sufficient knowledge about the topic, return `true`.  
   - If you need external information that is not available in your training data, return `false`.  

2. **Accuracy and Reliability:**  
   - If you can write a precise, comprehensive, and reliable article, return `true`.  
   - If your knowledge on the topic is incomplete or unreliable, return `false`.  

3. **Need for Updated Data:**  
   - If writing the article requires recent data (e.g., latest statistics, news, or studies published after your last update), return `false`.  
   - If the available information is sufficient without requiring the latest updates, return `true`.  

4. **Complex Analysis or Computations:**  
   - If the article requires complex analysis or calculations that you cannot perform, return `false`.  
   - If the content can be generated without such advanced processing, return `true`.  

5. **Restricted or Sensitive Topics:**  
   - If the article involves restricted, unethical, or policy-violating topics, return `false`.  
   - Otherwise, return `true`.  

**Input:**  
Article title: "[Insert article title here]"  

**Output should only be `true` or `false`, with no additional text.**  
"""},
            {"role": "user", "content": title}
        ]
    )

    return response.choices[0].message.content


