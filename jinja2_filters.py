import base64

def b64encode(string):
	if type(string) == str:
		return base64.b64encode(
			string.encode('utf-8')
		).decode('utf-8')
	return base64.b64encode(string).decode('utf-8')