# Forge Fitness Module

## Installation
### Docker Compose

Prerequisites
- Forge-Core must be installed and setup

#### Steps
1. Launch the following docker services
```yaml
services:
  fitness-module:
    image: forge-project/forge_fitness-panel:latest
    container_name: Forge_Fitness-Module
    environment:
      - DATABASE_URL=DATABASE_URL=postgresql+asyncpg://user:<your_password>@localhost/db
      - FORGE_SECRET=<your_secret>

  database:
    image: postgres
    container_name: Forge_Fitness-Database
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=<your_password>
      - POSTGRES_DB=db
```
_Note: The Fitness Module must be inside the same network of the Core Service_

## Development documentation
- [Uvicorn (Web server)](https://www.uvicorn.org/)
- [FastAPI (ASGI framework)](https://fastapi.tiangolo.com/)
- [SQLModel (SQLAlchemy/pydantic ODM)](https://sqlmodel.tiangolo.com/)


### Setup project

Prerequisites
- Python 3.10+
- SQL connection

#### Steps
1. Clone repository
```shell
git clone https://github.com/Forge-Panel/Fitness-Module.git
```

2. Create virtual environment
```shell
python -m venv <venv>
```

3. Activate environment
```shell
# Linux / Mac
source <venv>/bin/activate

# Windows
<venv>\Scripts\activate.bat
```

4. Install requirements
```shell
pip install -r requirements.txt
```

5. Set environment variables
```shell
export DATABASE_URL={dialect+driver://username:password@host:port/dbname}
export DEBUG=true
```

6. Start docker services
```shell
docker compose -f docker-compose.dev.yml up
```

7. Start development servers
```shell
uvicorn app:app --reload
```


### Docker

Prerequisites
- Docker

#### Steps
1. Build Docker image
```shell
docker build --build-arg="PYTHON_VERSION=3.x" --tag="forge-project/forge_fitness-panel:latest"
```
_Note: You must use Python version >= 3.10!_

2. Push to the Docker registry
```shell
docker image push forge-project/forge_fitness-panel:latest
```