# NGINX with Proxy Generator

It allows us to start :

1. a Nginx instance
2. generate proxy configurations
3. generate basic auth

The application can be managed via:
1. `manage.sh`
2. or manually as explained below


## Manage via `manage.sh`

```bash
usage manage.sh [clean_conf | gen_default | gen_all | start | restart | reload | stop]
```
options:

1. clean_conf: remove all the configuration from `nginx/conf.d/`
2. gen_default: generate only the `default.conf` file
3. gen_all: generate all the configurations files from the `nginx_conf.json` file
4. start: start the docker container of nginx
5. restart: restart the docker container
6. reload: reload the configuration in `nginx/conf.d/`
7. stop: stop the container and clean the current folder

## Manual Configurations

### Reload NGINX confs

```bash
docker exec -it <container_name> /usr/sbin/nginx -t  
```

### Start NGINX

```bash
docker-compose up -d
```

### Generate Proxy configurations

The python script `nginxify.py` can be used to generate `*.conf` files.

```bash

./nginxify.py --help

usage: nginxify.py [-h] [--default ONLY_DEFAULT] [--dest DEST_FOLDER]
                   [--conf CONFS_FILE] [--overwrite OVERWRITE]

nginx conf generator

optional arguments:
  -h, --help            show this help message and exit
  --default ONLY_DEFAULT
                        if true generate only the default configurations
  --dest DEST_FOLDER    The folder to save the *.conf files. Default value
                        './nginx/conf.d/'
  --conf CONFS_FILE     The json file with the configurations. Default value
                        'nginx_conf.json'
  --overwrite OVERWRITE
                        True to overwrite all the configurations files
```

#### Json File Structure
The file contains a list of `proxies` with:
- **name**: the name of the proxy
- **server_names**: the name of the domain name to expose the service
- **docker_name**: the name or ip address of the docker container to expose
- **docker_port**: the internal port of the container
- **secured**: if the service should be secured with [nginx auth_basic]()

```json

{
  "proxies": [
    {
      "name": "spark",
      "servers": [
        "spark.datatoknowledge.it"
      ],
      "dockers": [
        "spark-master-0:8080"
      ],
      "secured": true
    },
    {
      "name": "es",
      "servers": [
        "es.datatoknowledge.it"
      ],
      "dockers": [
        "es-data-0:9200",
        "es-data-1:9200",
        "es-data-1:9200"
      ],
      "docker_name": "es-data-0",
      "docker_port": "9200",
      "secured": true
    },
    {
      "name": "datatoknowledge",
      "servers": [
        "datatoknowledge.it",
        "www.datatoknowledge.it"
      ],
      "dockers": [
        "dtk-0:5000"
      ],
      "secured": false
    }
  ]
}

```

### Password generator

The script `password_generator.py` can be used to generate a file that stores the access passwords. By default it stores all the password in `/nginx/htpasswd/secure`. This file is mapped to the running docker container.

#### Usage

```bash
./password_generator.py --help
usage: password_generator.py [-h] [--file DEST_FOLDER] [--user USER]
                             [--pwd PWD]

nginx auth file generator

optional arguments:
  -h, --help          show this help message and exit
  --file DEST_FOLDER  the folder to save the new username:password pair
  --user USER         the username for the new user
  --pwd PWD           the password for the new user
```

### Index 404 and 50x pages

As default there is a custom_404 custom_50x and index page in the folder `./nginx/www/html`. If you need you can change these pages.
