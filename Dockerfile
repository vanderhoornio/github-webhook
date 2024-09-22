FROM python:3.12.0
# FROM insertcoinshere/dexbots:dexnet

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Install pip requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Run the app in development
CMD ["python", "run.py"]

# Run the app in production
# CMD ["gunicorn", "--bind", "0.0.0.0:443", "--certfile", "/usr/local/share/ca-certificates/ca-certificates.crt", "run:app"]