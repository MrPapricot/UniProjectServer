import json

import requests

token = "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"

headers = {
	'Authorization': f'token {token}'
}

# Отправка GET-запроса на эндпоинт для получения информации о пользователе
response = requests.get('https://api.github.com/user', headers=headers)

# Если запрос прошел успешно, выводим имя пользователя
if response.status_code == 200:
	user_info = response.json()
	with open("ggg.json", 'w') as file:
		json.dump(user_info, file)
	print(f'Имя пользователя: {user_info["login"]}')
else:
	print(f'Ошибка: {response.status_code}, {response.text}')
