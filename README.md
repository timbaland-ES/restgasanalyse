# Restgasanalyse

This is a student project during my master study for the "GSI Helmholzzentrum für Schwerionenforschung". They maintain a particle accelerator for ions (Teilchenbeschleuniger für Ionen).
They had difficulties at analyzing the concentrations of material in the accelerator. 
Therefore we created a system that takes the measured datas, stores them, and visualize them remotely. So they now have much better opportunities to analyze the measured data. 

![image](https://github.com/timbaland-ES/restgasanalyse/assets/77269620/34bb5f5b-6863-4cf2-8c34-24f6029e4c57)


## Systemarchitektur

![image](https://github.com/timbaland-ES/restgasanalyse/assets/77269620/2869cde6-a19f-4cee-a0fb-38cbda16d5d3)




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
