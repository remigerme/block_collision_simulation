import json


def get_config():
	"""
	There is no error handling for now, be careful with config.json.
	"""
	with open("config.json", "r") as f:
		config_settings = json.load(f)
	return config_settings
