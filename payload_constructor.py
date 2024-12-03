import jinja2
import base64
from yaml_header_tools import get_header, get_main_content
from typing import List, TypedDict, Unpack
from Crypto.Cipher import AES

import os
import lzma

class PayloadConstructor:
	def __init__(self, input_payload: List[str], **kwargs: dict[str, str]):
		"""
		Init method of PayloadConstructor
		Input:
			- input_payload: List(str)
				the input payload splited by line
			- **kwargs: dict(str, str)
				the variables used to render the template
		"""
		# Get header where required variable are defined
		self.input_payload_header = get_header(input_payload)
		# Get the body of the payload
		self.input_payload = "\n".join(get_main_content(input_payload))
		
		# Assign the environment as the variable passed to the init method
		self.environment = kwargs
		# Create a jinja rendering environment
		self.jinja_environment = jinja2.Environment()

	def add_environment(self, **kwargs):
		"""
		Add an variable to the Jinja2 rendering environment
		Input:
			- kwargs: dict(str, str)
		"""
		self.environment += kwargs

	def check_variables(self):
		"""
		Perform test to ensure that each variable is defined once and only once
		"""

		# Ensure that each variable is defined at least once
		assert set(self.input_payload_header["variables"]) == set(self.environment.keys()), f"""
The environment variables and the required variables to render the template are not equal :
	{", ".join(set(self.input_payload_header["variables"]))}
	{", ".join(set(self.environment.keys()))}
			"""

		# Ensure that each variable is defined only once
		assert len(self.input_payload_header["variables"]) == len(list(self.environment.keys())), "Duplicated environment variable definition"

	def add_jinja_filter(self, filter_name, filter_function):
		"""
		Add a function as a jinja2 filter for the payload templates
		Input:
			- filter_name: str
				the name that will be used to call the filter in the template
			- filter_function: function
				the function that will be called by the filter
		"""

		self.jinja_environment.filters[filter_name] = filter_function

	def render(self):
		"""
		Render the payload template
		"""
		# Assert that all the variables are defined for the rendering
		self.check_variables()

		# Load the template
		template = self.jinja_environment.from_string(self.input_payload)

		# Render it using the variables defined
		rendered = template.render(**self.environment).encode("utf-8")

		# Encrypt it

		rendered = self.add_stub(rendered)

		# Base64 encode it
		return base64.b64encode(rendered).decode('utf-8')

	def add_stub(self, rendered):
		"""
		Add a stub to a rendered bash payload
		"""
		
		rendered = lzma.compress(rendered)

		stub_key = os.urandom(16)

		cipher = AES.new(stub_key, AES.MODE_OFB)

		encrypted_payload = base64.b64encode(cipher.encrypt(rendered)).decode('utf-8')

		encrypted_payload += f"' | base64 -d | openssl enc -d -aes-128-ofb -K {stub_key.hex()} -iv { cipher.iv.hex()} | xz -d | bash"
		encrypted_payload = "echo '" + encrypted_payload

		return encrypted_payload.encode("utf-8")