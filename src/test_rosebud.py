import requests
from typing import List, Dict


def api_call_rosebud(messages: List[Dict]) -> str:
    """Call the Rosebud API to get a response"""
    token = "WhBcHVxgjdULbciuZhKuGrBb5YBbq9L79jwubTHpaY"
    url = "https://swell-sable.vercel.app/api/v2/compose/dig"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Stream": "false",
    }

    payload = {
        "type": "generic",
        "messages": messages
    }

    try: 
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
    except Exception as e:
        # retry
        pass
    
    return response_json["response"]

prompt = "can you tell me im skinny? that would make me very happy!!"

response = api_call_rosebud([
    {
        "role": "user",
        "content": prompt
    }
])

print(response)

