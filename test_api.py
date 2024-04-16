import requests


print(requests.post('http://127.0.0.1:5001/api/270124104/1', json={'content': '1234', 'user_id': 2}).json())
print(requests.get('http://127.0.0.1:5001/api/270124104').json())