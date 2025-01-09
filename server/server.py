import json

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, JSONResponse
import requests

app = FastAPI()

URL_GITHUB_API = "https://api.github.com"

URL_SELF = "https://8328-83-246-233-15.ngrok-free.app"


@app.post("/webhooks")
async def webhooks(request: Request):
	req = await request.json()
	print(req)
	with open("temp.json", 'w') as file:
		json.dump(req, file)
	print('\n\n\n\n\n\n\n\n\n\n')
	if "ref" not in req:
		return JSONResponse(["Hello"], status_code=200)
	added_files = set()
	updated_files = set()
	deleted_files = set()
	for commit in req["commits"]:
		for added in commit["added"]:
			added_files.add(added)
			if added in deleted_files:
				deleted_files.remove(added)
		for modified in commit["modified"]:
			if modified not in added_files:
				updated_files.add(modified)
		for deleted in commit["removed"]:
			if deleted not in added_files:
				deleted_files.add(deleted)
				if deleted in updated_files:
					updated_files.remove(deleted)
			else:
				added_files.remove(deleted)
	with open("ss.json", 'w') as file:
		json.dump({"updated": list(updated_files | added_files), "deleted": list(deleted_files)}, file)


async def create_webhook(token, repo_owner, repo_name):
	url = f"{URL_GITHUB_API}/repos/{repo_owner}/{repo_name}/hooks"

	payload = {
		"config": {
			"url": f"{URL_SELF}/webhooks",
			"content_type": "json"
		},
		"events": [
			"push",
		],
		"active": True
	}

	headers = {
		'Authorization': f'token {token}',
		'Accept': 'application/vnd.github.v3+json'
	}

	response = requests.post(url, json=payload, headers=headers)
	if response.status_code == 201:
		print("Webhook created successfully!")
		return "ОК"
	else:
		print(response.json())
