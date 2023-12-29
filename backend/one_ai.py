import requests

def oneAi_summary(oneAi_token, messages, skill): # message is in {name: message} form
    url = "https://api.oneai.com/api/v0/pipeline"
  
    headers = {
        "api-key": oneAi_token, 
        "content-type": "application/json"
    }
    payload = {
        "input": messages,
        "input_type": "conversation",
        "content_type": "application/json",
        "output_type": "json",
        "multilingual": {
            "enabled": True
        },
        "steps": [
            {
                "skill": skill
            }
        ],
    }
    try:
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()
        print(data)
        return data['output'][0]['contents'][0]['utterance']  # text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
    except KeyError as e:
        print(f"Key error in parsing response: {e}")
    except IndexError as e:
        print(f"Index error in parsing response: {e}")
    return None
