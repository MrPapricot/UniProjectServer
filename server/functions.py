import base64
import json

import requests

from server import URL_GITHUB_API
from CustomErrors import *

test_token = "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"
wrong_token = "ghp_dLP0TLqDaDagAoqmdFWcpFNkDqWKpo2142Bj"


def get_user_name(token):
	headers = {
		'Authorization': f'token {token}'
	}

	response = requests.get(f"{URL_GITHUB_API}/user", headers=headers)

	if response.status_code == 200:
		user_info = response.json()
		return user_info["login"]
	else:
		if response.status_code == 401:
			response_json = response.json()
			if response_json["message"] == "Bad credentials":
				raise InvalidTokenException()
		else:
			raise Exception()


def get_user_repos(token):
	headers = {
		'Authorization': f'token {token}'
	}
	response = requests.get(f"{URL_GITHUB_API}/user/repos", headers=headers)

	if response.status_code == 200:
		repository_names = []
		for repository_info in response.json():
			repository_names.append(repository_info["name"])
		return repository_names
	else:
		if response.status_code == 401:
			repos_info = response.json()
			if repos_info["message"] == "Bad credentials":
				raise InvalidTokenException()
		else:
			raise Exception()


def get_files(token, username, projectname, filepaths):
	headers = {
		'Authorization': f'token {token}'
	}
	base_url = f"{URL_GITHUB_API}/repos/{username}/{projectname}/contents"
	texts = []
	for path in filepaths:
		url = f"{base_url}/{path}"
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			file_info = response.json()
			texts.append(base64.b64decode(file_info["content"]).decode("utf-8"))
	return texts


print(*get_files(test_token, get_user_name(test_token), "TEST", ["Hello World.txt", "ahsh/rgsahsh.txt"]), sep="\n--------------\n")
