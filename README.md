<p align="center">
  <a href="https://github.com/Forge-Panel" target="blank"><img src="https://raw.githubusercontent.com/Forge-Panel/.github/refs/heads/main/images/forge_logo_dark_bg.svg" width="512" alt="Forge Logo" /></a>
</p>
<h1 align="center">Fitness</h1>

<p align="center">Forge-Fitness is an open source module to keep track of your fitness statistics.</p>
<p align="center"><i>This repository is for the backend made with FastAPI</i></p>


## Installation
### Docker Compose

Prerequisites
- Docker installed

#### Steps
1. Launch the following docker services
```yaml
services:
  fitness-module:
    image: forge-project/forge_fitness-panel:latest
    container_name: Forge_Fitness-Module
    environment:
      - DATABASE_URL=DATABASE_URL=postgresql+asyncpg://<db_user>:<db_password>@localhost/<db_database>

  database:
    image: postgres
    container_name: Forge_Fitness-Database
    environment:
      - POSTGRES_USER=<db_user>
      - POSTGRES_PASSWORD=<db_password>
      - POSTGRES_DB=<db_database>
```

2. Connect the app to your instance
3. Done!
<br />

## Documentation

### Frameworks
- [Uvicorn (Web server)](https://www.uvicorn.org/)
- [FastAPI (ASGI framework)](https://fastapi.tiangolo.com/)
- [SQLModel (SQLAlchemy/pydantic ODM)](https://sqlmodel.tiangolo.com/)

<br />

### Project setup

Prerequisites
- Python 3.10+
- SQL connection

#### Setup development
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
export APP_DEBUG=true
```

6. Start docker services
```shell
docker compose -f docker-compose.dev.yml up
```

7. Start development servers
```shell
uvicorn app:app --reload
```

<br />

### Build Docker image

Prerequisites
- Docker installed

#### Steps
1. Build Docker image
```shell
docker build --build-arg="PYTHON_VERSION=3.12" --tag="forge-project/forge_fitness-panel:latest"
```
_Note: You must use Python version >= 3.10!_

2. Push to the Docker registry
```shell
docker image push forge-project/forge_fitness-panel:latest
```