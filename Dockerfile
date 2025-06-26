ARG PYTHON_VERSION=3.12

# build stage
FROM python:${PYTHON_VERSION}-alpine
LABEL authors="Spider Frog"

# Set the working directory to /app
WORKDIR /app

# Install the dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app/ .
ADD models/ .
ADD sharables/ .

EXPOSE 8000

# run the command to start uvicorn
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--workers", "4", "--port", "8000", "api:app"]