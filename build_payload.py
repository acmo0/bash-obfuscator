import argparse
import sys
import base64
from payload_constructor import PayloadConstructor
import yaml

from jinja2_filters import *

parser = argparse.ArgumentParser(
    prog='build_payload',
    description='Render a Jinja2 template of bash script',
    epilog='This is fur educationnal purpose only'
)

parser.add_argument(
    "payload_template",
    type=argparse.FileType('r'),
    default=sys.stdin,
    nargs="?"
)
parser.add_argument(
    "-e",
    "--environment",
    nargs="+",
    metavar=("name", "value"),
    action="append"
)
parser.add_argument(
    "-f",
    "--file",
    type=argparse.FileType('r')
)
parser.add_argument(
    '-o',
    '--output',
    nargs='?',
    type=argparse.FileType('w'),
    default=sys.stdout
)

args = parser.parse_args()

environment = {}

if args.file and args.environment:
    print("ERROR : -f/--file and -e/--environment are exlusive, don't use both")
    exit()
elif not (args.file or args.environment):
    print("ERROR : -f/--file or -e/--environment should be set")
    exit()
elif args.file:
    environment = yaml.safe_load(args.file.read())
else:
    for variable_name, *variable_value in args.environment:
        if variable_name in environment.keys():
            print(f"ERROR : Duplicated environment variable definition : {variable_name}")
            exit()
        if len(variable_value) == 1:
            environment[variable_name] = variable_value[0]
        else:
            environment[variable_name] = variable_value

# Read template from buffer
input_payload = args.payload_template.read()

template_renderer = PayloadConstructor(
    input_payload=input_payload.split("\n"),
    **environment
)

template_renderer.add_jinja_filter("b64encode", b64encode)

rendered_template = template_renderer.render()

args.output.write(rendered_template)