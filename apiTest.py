import requests as req
import json

url = 'http://api.stackexchange.com/2.2/search/advanced'

params = {'q': 'Access internet using wifi',
			'site': 'stackoverflow',
			'order': 'desc',
			'sort': 'activity'}

data = req.get(url=url, params=params).json()['items']

print(len(data))
'''
answers = {}
for i, answer in enumerate(data):
	answers[i] = {}
	answers[i]['tags'] = answer['tags']
	answers[i]['title'] = answer['title']
	answers[i]['is_answered'] = answer['is_answered']
	answers[i]['link'] = answer['link']'''
with open('result.json', 'w') as f:
	f.write(json.dumps(data, indent=2))