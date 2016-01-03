#!/usr/bin/env python
import json
import os
import argparse

nginx_conf_template = """
#Websocket conf
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

# ex sub_domain.domain.it
# proxy_name
upstream %s {
            # docker_name:port
%s
}

server {
        gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;

        # server_names
%s
        proxy_buffering off;
        error_log /proc/self/fd/2;
        access_log /proc/self/fd/1;

        location / {
                resolver 8.8.8.8 valid=30s;
                # sub_domain, domain
                proxy_pass http://%s;
                proxy_set_header Host $http_host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;

                # HTTP 1.1 support
                proxy_http_version 1.1;
                proxy_set_header Connection "";
                # Websocket conf
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";

                %s
        }
}
"""

secured_template = """
                # Optional, only if the app need authentication.
                auth_basic    "Restricted %s";
                auth_basic_user_file /etc/nginx/htpasswd/secure;
"""

def generate_server_names(array):
    template = "        server_name %s;\n"
    result = ""
    for n in array:
        result += template % n

    return result

def generate_upstream_servers(array):
    template = "            server %s;\n"
    result = ""
    for n in array:
        result += template % n

    return result

def generate_proxy_conf(proxy_name, servers, dockers, secured):

    servers_names = generate_server_names(servers)
    upstream_servers = generate_upstream_servers(dockers)

    secured_str = ""
    if secured:
        secured_str = secured_template % (servers[0])

    parameters = (proxy_name, upstream_servers, servers_names, proxy_name,
        secured_str)
    nginx_proxy = nginx_conf_template % parameters
    return nginx_proxy

def generate_configurations(json_data, dest_folder, overwrite):
    for proxy in json_data['proxies']:
        conf = generate_proxy_conf(proxy['name'], proxy['servers'],
            proxy['dockers'],proxy['secured'])
        file_path = dest_folder + proxy['name'] + ".conf"

        if overwrite:
            print("generating confs for", proxy['name'])
            with open(file_path, 'w') as out:
                out.write(conf)
        elif not os.path.exists(file_path):
            print("generating confs for", proxy['name'])
            with open(file_path, 'w') as out:
                out.write(conf)


def generate_default(dest_folder):
    default_template =  """server {
        listen 80 default_server;
        listen [::]:80 default_server ipv6only=on;


        error_page 404 /custom_404.html;
        location = /custom_404.html {
                root /usr/share/nginx/html;
                internal;
        }

				error_page 500 502 503 504 /custom_50x.html;
				location = /custom_50x.html {
								root /usr/share/nginx/html;
								internal;
				}
}
    """

    #create default_server
    default_path = dest_folder + "default.conf"
    if not os.path.exists(default_path):
        print("generating confs for default")
        with open(default_path, 'w') as f:
            f.write(default_template)

def str2bool(v):
  return v.lower() in ("True", "true", "t")

def main():
    parser = argparse.ArgumentParser(description="nginx conf generator")
    parser.add_argument('--default', dest='only_default', default='False',
        help='if true generate only the default configurations')
    parser.add_argument('--dest', dest='dest_folder', default='./nginx/conf.d/',
        help="The folder to save the *.conf files. Default value './nginx/conf.d/'")
    parser.add_argument('--conf', dest='confs_file', default='nginx_conf.json',
        help="The json file with the configurations. Default value 'nginx_conf.json'")
    parser.add_argument('--overwrite', dest='overwrite', default='True',
        help="True to overwrite all the configurations files")

    args = parser.parse_args()

    if not os.path.exists(args.dest_folder):
        os.makedirs(args.dest_folder)

    if str2bool(args.only_default):
        generate_default(args.dest_folder)
    else:
        generate_default(args.dest_folder)
        #read configurations and create conf files
        f = open(args.confs_file)
        json_data = json.load(f)
        f.close()
        generate_configurations(json_data, args.dest_folder, str2bool(args.overwrite))

if __name__ == '__main__':
    main()
