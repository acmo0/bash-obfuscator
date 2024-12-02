import jinja2
import base64
from yaml_header_tools import get_header, get_main_content
from typing import List, TypedDict, Unpack

class PayloadConstructor:
	def __init__(self, input_payload: List[str], **kwargs: str):
		self.input_payload_header = get_header(input_payload)
		self.input_payload = "\n".join(get_main_content(input_payload))
		self.environment = kwargs
		self.jinja_environment = jinja2.Environment()

	def add_environment(self, **kwargs):
		self.environment += kwargs

	def check_variables(self):
		assert set(self.input_payload_header["variables"]) == set(self.environment.keys()), f"""
The environment variables and the required variables to render the template are not equal :
	{", ".join(set(self.input_payload_header["variables"]))}
	{", ".join(set(self.environment.keys()))}
			"""
		assert len(self.input_payload_header["variables"]) == len(list(self.environment.keys())), "Duplicated environment variable definition"

	def add_jinja_filter(self, filter_name, filter_function):
		self.jinja_environment.filters[filter_name] = filter_function

	def render(self):
		self.check_variables()

		template = self.jinja_environment.from_string(self.input_payload)

		rendered = template.render(**self.environment).encode('utf-8')

		return base64.b64encode(rendered).decode('utf-8')
