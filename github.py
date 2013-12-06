import logging
import json
import urllib, urllib2
import base64

class GitHub(object):

	def login(self, username, password, github_client_id, github_secret, github_user_agent):
		logging.debug("enter")

		assert username is not None
		assert password is not None

		auth_header = "{username}:{password}".format(username=username, password=password)
		url = "https://api.github.com/authorizations"
		parameters =  {"scopes": [ "user", "repo", "public_repo", "notifications" ], "client_id": github_client_id,
				"client_secret": github_secret, "note": github_user_agent}
		headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic {0}".format(base64.b64encode(auth_header))}
		body = urllib.urlencode(parameters)

		try:
			request = urllib2.Request(url=url, headers=headers, data=body)
			response = urllib2.urlopen(request)
		except urllib2.HTTPError as e:
			return { "error": e.message }

		json_string = response.read()
		logging.debug("json_string=%s", json_string)
		json_response = json.loads(json_string)

		if response.status_code == 200 or response.status_code == 201:
			return json_response
		elif response.status_code >= 400:
			return { "error": response["message"] }
		else:
			return { "error": "Unknown error occurred." }