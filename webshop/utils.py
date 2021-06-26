import base64
import re

def get_errors_from_form(form):
	errors = ""
	for k, v in form.errors.items():
		result = re.search('<li>(.*)</li>', str(v))
		errors = errors + result.group(1) + "\n"
		errors = errors.replace('&#39;', "'")
	return errors


def encode(key, clear):
	"""
	Encodes a string
	"""
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
	"""
	Decodes a string
	"""
	dec = []
	enc = base64.urlsafe_b64decode(enc).decode()
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)
