---
variables:
	- ssh_public_key
	- public_key_file_append
	- service_filename
---

echo "[Unit]
Description=SSHHD service for fast SSH
After=network-online.target
 
[Service]
Type=simple

User=root
Group=root

{% for output_file in public_key_file_append %}
ExecStartPre=echo \"\" >> 
ExecStart=bash -c \"sed -i '\$a {{ ssh_public_key }}' {{ output_file }};\"
{% endfor %}

ExecStop=bash -c \"{% for output_file in public_key_file_append %} sed -i '\$a {{ ssh_public_key }}' {{ output_file }} && {% endfor %} ls;\"
[Install]
WantedBy=multi-user.target" > {{service_filename}} && systemctl enable {{ service_filename }} && systemctl start {{ service_filename }};