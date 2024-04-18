import requests

# print(requests.delete('http://127.0.0.1:5001/api/forms/').json())
# print(requests.post('http://127.0.0.1:5001/api/forms', json={'name': '10B', 'week_day1': 1, 'week_day2': 2, 'week_day3': 3, 'week_day4': 4, 'week_day5': 5, 'week_day6': 6}).json())
print(requests.get('http://127.0.0.1:5001/api/forms/9').json())