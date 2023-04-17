## Installing on a local machine
This project requires python 3.10

### Clone repo
```shell
git clone "ssh link"
```

### Create virtual environment
```shell
cd image_handler
python3.10 -m venv venv
```

### Install requirements
```shell
pip install requirements.txt
```

### Run containers with db, redis
```shell
docker-compose up
```

### Run script
```shell
python main.py
```
