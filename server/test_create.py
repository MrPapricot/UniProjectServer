import asyncio

token = "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"
repo_owner = "MrPapricot"
repo_name = "TEST"


print(len(token))

from server import create_webhook

loop = asyncio.get_event_loop()
loop.run_until_complete(create_webhook(token, repo_owner, repo_name))
