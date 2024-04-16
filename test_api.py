import requests

print(requests.post('http://127.0.0.1:5001/api/270124103/1', params={'content': '1234', 'user_id': 1}).json())