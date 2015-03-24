# Automatically prompt if there are updates.
import urllib2, json, pprint

user = "internetimagery"
repo = "license_fix"

response = urllib2.urlopen("https://api.github.com/repos/%s/%s/releases/latest" % (user, repo))
html = response.read()
if html:
	data = json.loads(html)
	result = {}
	result["version"] = data["tag_name"]
	result["date"] = data["created_at"]
	result["download"] = data["zipball_url"]
	print pprint.pprint(result)

