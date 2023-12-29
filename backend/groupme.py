import requests
from datetime import datetime, timedelta

    # reference -> https://dev.groupme.com/

# fetch group ids and group informations
def fetchGroupData(access_token):
    url = 'https://api.groupme.com/v3/groups'
    headers = {
        'Content-Type': 'application/json',
        'X-Access-Token': access_token,
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get groups. Status code: {response.status_code}")
        return None

# fetching group messages 
def getMessages(access_token, group_id):
    url = f"https://api.groupme.com/v3/groups/{group_id}/messages"
    
    # Change for different time periods
    one_week_ago = datetime.now() - timedelta(weeks=1)
    one_day_ago = datetime.now() - timedelta(days=1)

    params = {
        'token': access_token,
        'limit': 100
    }

    all_messages = []
    fetch_more = True

    while fetch_more:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()['response']
            messages = data['messages']

            if messages:
                last_message_time = datetime.utcfromtimestamp(messages[-1]['created_at'])
                fetch_more = last_message_time > one_week_ago
                params['before_id'] = messages[-1]['id']
                
                for message in messages:
                    message_time = datetime.utcfromtimestamp(message['created_at'])
                    # if message_time > one_day_ago:
                    if message_time > one_week_ago:
                        message_info = {
                            'id': message['id'],
                            'group_id': message['group_id'],
                            'name': message['name'],
                            'text': message['text'],
                            'created_at': datetime.utcfromtimestamp(message['created_at'])
                        }
                        all_messages.append(message_info)
                    else:
                        fetch_more = False
                        break
        elif response.status_code == 304:
            print('No more messages found')
            break
        else:
            print("Error:", response.status_code, response.text)
            fetch_more = False
    
    return all_messages
        
# format message
def formatMessages(messages_from_db):
    formatted_messages = []
    for message in messages_from_db:
        try:
            speaker = message.get("name","")
        except KeyError:
            speaker = "Unknown"
        utterance = message.get("text", "")
        formatted_message = {"speaker": speaker, "utterance": utterance}
        formatted_messages.append(formatted_message)

    return formatted_messages