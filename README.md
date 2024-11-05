# Forge Fitness Module

## Setup 

## Development documentation
- [Uvicorn (Web server)](https://www.uvicorn.org/)
- [FastAPI (ASGI framework)](https://fastapi.tiangolo.com/)
- [SQLModel (SQLAlchemy/pydantic ODM)](https://sqlmodel.tiangolo.com/)


### Setup project

Prerequisites
- Python 3.10+
- SQL connection

Clone repository
```shell
git clone https://github.com/Forge-Panel/Fitness-Module.git
```

Create virtual environment
```shell
python -m venv <venv>
```

Activate environment
```shell
# Linux / Mac
source <venv>/bin/activate

# Windows
<venv>\Scripts\activate.bat
```

Install requirements
```shell
pip install -r requirements.txt
```

Set environment variables
```shell
export DATABASE_URL={dialect+driver://username:password@host:port/dbname}
export DEBUG=true
```

Start docker services
```shell
docker compose -f docker-compose.dev.yml up
```

Start development servers
```shell
uvicorn app:app --reload
```


### Docker

Prerequisites
- Docker

Build Docker image
```shell
docker build --build-arg="PYTHON_VERSION=3.x" --tag="forge-project/forge_fitness-panel:latest"
```
_Note: You must use Python version >= 3.10!_

Push to the Docker registry
```shell
docker image push forge-project/forge_fitness-panel:latest
```