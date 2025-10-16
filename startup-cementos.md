# Postgres

## Build (on compose/dev/postgres)
```
sudo podman build --tag krm_postgres .
```
## Run
```
sudo podman run -d -p 5432:5432 --name krm_postgres --network host --env-file .envs/.dev/.postgres --volume krm_postgres_data:/var/lib/postgresql/data --volume krm_postgres_data_backups:/backups krm_postgres  -c listen_addresses='*'
```

# Django

## Build (on project root folder)
```
sudo podman build --tag krm_django .
```
## Run
```
sudo podman run -d -p 8000:8000 --name krm_django --network host --env-file .envs/.dev/.all --volume .:/app krm_django
```

# Nginx

## Build
```
sudo podman build --tag krm_nginx .
```

## Run
```
sudo podman run -d -p 80:80 -p 443:443 --name krm_nginx --network host krm_nginx
```


# Util Commands

## Get container IP
```
sudo podman inspect -f '{{.NetworkSettings.IPAddress}}' <container>
```
## Open container terminal
```
sudo podman exec -ti <command_id> /bin/sh
```

