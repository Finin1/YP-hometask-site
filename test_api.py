import requests

# print(requests.delete('http://127.0.0.1:5001/api/forms/').json())
print(requests.post('http://127.0.0.1:5001/api/homeworks/150420249/1', json={'content': 'test', 'user_id': 1}).json())
print(requests.get('http://127.0.0.1:5001/api/homeworks/150420249/1').json())
