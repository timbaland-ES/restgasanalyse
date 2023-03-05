# Restgasanalyse

## Development
```bash
docker-compose up -f scripts/docker-compose.yml
# maybe you need to change the permissions on shared forder ./scripts/grafana 
# chmod
```

## Development Installation 

```bash
# 1 Install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker <your_user>

# 2 Install docker-compose
pip install docker-compose

# 3 install postgres driver and python client
sudo apt install libpq-dev
pip install psycopg2

# 4 Install other requirements
pip install -f requirements.txt

# 5 Datasource in Grafana einrichten (später automatisieren)
```



## Production Installation 

```bash
# 1 Install postgres and grafana
# https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/
# https://pimylifeup.com/raspberry-pi-postgresql/

# 2 install postgres driver and python client
sudo apt install libpq-dev
pip install psycopg2

# 3 Install other requirements
pip install -f requirements.txt
```


## TODO: 
* systemctl Linux Service für restgasanalyse
