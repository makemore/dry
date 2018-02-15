# 1063487350460910/feed?fields=story,updated_time,id,message,place,picture,attachments
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import os, requests, json, facebook

"""
def get_fb_token(app_id, app_secret):
	payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
	file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
	# print file.text #to test what the FB api responded with
	# result = file.text.split("=")[1]
	# print file.text #to test the TOKEN
	data = json.loads(file.text)
	return data["access_token"]


print(os.environ.get("FB_APP_ID"), os.environ.get("FB_APP_SECRET"))
token = get_fb_token(os.environ.get("FB_APP_ID"), os.environ.get("FB_APP_SECRET"))

print(token)

graph = facebook.GraphAPI(access_token=token, version="2.7")
"""
import pprint

pp = pprint.PrettyPrinter(indent=4)


def process_page_of_data(data):
	for post in data:
		print(post["id"])
		print(post["message"])
		#pp.pprint(post)


# print(post["message"])


headers = {
	'authorization': "Bearer " + os.environ.get("FB_USER_TOKEN"),
	'content-type': "application/json",
}

payload = requests.get(
	"https://graph.facebook.com/v2.12/1063487350460910/feed?fields=story,updated_time,id,message,place,picture,attachments&limit=1",
	headers=headers)

result = json.loads(payload.text)

process_page_of_data(result["data"])
