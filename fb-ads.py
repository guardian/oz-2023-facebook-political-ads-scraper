#!/usr/bin/env python3
# -*- coding: utf-8 -*-

advertisers = [
	{"name":"Yes23", "id":102329728050606},
	{"name":"Fair Australia", "id":104180525925926},
	{"name":"Senator Jacinta Nampijinpa Price","id":1622506634677043}]

import requests

token = "EAArd4ZCxT9FkBAO9QOPlLvHw6ZBXn19TSnLqjuZBFVAd33RTU67Gb9LfaEbGjVXtTZACEHFrPyiFiN6lIK36muawfKW8EAZAgZCiLZAMch6XxjKEIZCDF9X0BIP1DoRMhg1Kye1ZAfgNbU2nBwG7dnlUWy4CmwvZBR2AFJiZByXnTtsBhwlk0mgCZBTtnHCAZANjh33aZCKmsWcwII9ZBlx1QoEbCpcXsI7KRoTuyR1bWo5mgSBwDZAsztlzAIOi4ak0UDppSlQZD"

def searchAPI(query, country):
	url = f"https://graph.facebook.com/v17.0/ads_archive/?search_terms='{query}'&ad_reached_countries=['{country}']&access_token={token}"
	print(url)
	r = requests.get(url)
	print(r.text)
	

searchAPI("the voice", "AU")