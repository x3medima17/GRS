import json

def gen_result(status,message,data=None):
	result = dict(
		status = status,
		message = message,
		data = data
		)
	return json.dumps(result)