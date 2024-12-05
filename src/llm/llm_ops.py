import requests
import os
import json


def query_llm(prompt:str, model="gpt-4o-mini"):
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "temperature": 0.2
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data), verify=False)    
    final_response = response.json()['choices'][0]['message']['content'].strip()
    print(final_response)   
    return final_response