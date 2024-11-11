
import requests
import json

API_KEY = "hypr-lab-xxxxxx" #'hypr-lab-xxxxx'

API_BASE = 'https://api.hyprlab.io/v1'
global textfortts
textfortts = ""
def decode_bytes(data):
    if isinstance(data, bytes):
        return data.decode('utf-8', errors='replace')
    elif isinstance(data, dict):
        return {decode_bytes(key): decode_bytes(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_bytes(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(decode_bytes(item) for item in data)
    return data


def ask_LLM(modelname, systemprompt, content,API_KEY, temperature=0.7, top_p=0.9, max_tokens=400, frequency_penalty=1.1, presence_penalty=1.1, streaming=False):
    print(modelname)

    # Construct the payload
    data = {
        "model": modelname,
        "messages": [
            {
                "role": "system",
                "content": systemprompt
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stream": streaming
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Send a POST request
    response = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=data, stream=streaming)
    
    if response.status_code == 200:
        if streaming:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8').split('data: ')[1])
                    if chunk['choices'][0]['finish_reason'] is not None:
                        break
                    content = chunk['choices'][0]['delta'].get('content', '')
                    full_response += content
                    print(content, end='', flush=True)
            return full_response
        else:
            assistant_message = response.json()['choices'][0]['message']['content']
            return assistant_message
    else:
        print("Error:", response.status_code, response.text)
        return None


'''
import requests

def ask_LLM(modelname, systemprompt, content, API_KEY, temperature, top_p, max_tokens, frequency_penalty, presence_penalty):
    # Construct the payload
    data = {
        "model": modelname,
        "messages": [
            {
                "role": "system",
                "content": systemprompt
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        #"top_p": top_p,
        #"frequency_penalty": frequency_penalty,
        #"presence_penalty": presence_penalty,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # URL updated to match the Together API endpoint
    API_BASE = "https://api.together.xyz/v1"
    # Send a POST request
    response = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=data)

    # Display the response (you can format this better if needed)
    if response.status_code == 200:
        assistant_message = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        return assistant_message
    else:
        print("Error:", response.status_code, response.text)
        return response.status_code
    
'''
# ask_LLM('NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO',
#                                               "You are a very smart very intelligence assistant who is very helpful.",
#                                               text, API_KEY, temperature=0.5, top_p=0.95, max_tokens=1000,
#                                               frequency_penalty=1.1, presence_penalty=1.1)

