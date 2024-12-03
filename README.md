# bash-payload
This repository's aim is to store some malicious bash payload to be executed by the C2 agent in the repository `mrw-client`.

This repository contains a tool to create a bash script using a template in order to change easily some parameters of the malicious scripts.

## Usage
```
usage: build_payload [-h] [-e name [value ...]] [-f FILE] [-o [OUTPUT]] [payload_template]

Render a Jinja2 template of bash script

positional arguments:
  payload_template

options:
  -h, --help            show this help message and exit
  -e name [value ...], --environment name [value ...]
  -f FILE, --file FILE
  -o [OUTPUT], --output [OUTPUT]
```
- `payload_template` : the path of the file to be rendered. If not provided, STDIN will be used
- `-o / --output OUPUT` : the output file to write the rendered template. If not provided, STDOUT will be used
- `-e / --environment` : the declaration of a variable used in the script template to be rendered. The first following argument will be used as the variable name and the next will be used a the value. If multiple successive values are given, the final value of the variable will be a list.
- `-f / --file FILE` : alternative to the previous option. This file will contain the declaration of the variables in YAML format.


## How it works ?
- Template rendering :
Malicious script template -> Template rendering -> XZ compression
	-> AES 128 CFB encryption -> base64 encoding
	-> Add payload to undo the operation and execute the script
- Decoding and execution :
Encoded payload -> base64 decode -> execution -> base64 decode
	-> decryption -> XZ decompression -> execution of the original payload
## How to do a script template
The template is rendered using Jinja2, [see the documentation](https://jinja.palletsprojects.com/en/stable/).

The template is made in two parts : a header and a body.

- Header part : this part is usefull to check if the user give all the variables needed to render the script. It is the first thing to write when creating a template. This is what a header should looks like :
```
---
variables: the_file_i_want_to_cat
---
```
- Body part : this part will be rendered using the variables declared in the header of the template. This has to be a bash script with Jinja2 templating. Here is an exemple :
```
cat {{ the_file_i_want_to_cat }}
```

This example script template should looks like :
```
---
variables: the_file_i_want_to_cat
---
cat {{ the_file_i_want_to_cat }}
```

** This is only for educational purposes **
