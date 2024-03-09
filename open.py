

with open('teams39update.txt', 'r') as fp:
	teams = [line.strip().split(',') for line in fp.readlines()]


import requests

url = f'https://www.sports-reference.com/cbb/schools/TEMP/men/2024.html'

for game in teams:
	if len(game) != 2:
		continue
	home,away = game
	url = url.replace('TEMP', home)
	res = requests.get(url)
	if not 200 <= res.status_code < 300:
		print(res.status_code)
		print(url)
	url = url.replace(home, away)
	res = requests.get(url)
	if not 200 <= res.status_code < 300:
		print(res.status_code)
		print(url)
	url = f'https://www.sports-reference.com/cbb/schools/TEMP/men/2024.html'
	
