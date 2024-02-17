# FROM alpine:latest

# RUN apk update
# RUN apk add py-pip
# RUN apk add --no-cache python3-dev 
# RUN pip install --upgrade pip

# WORKDIR /app
# COPY . /app
# RUN pip --no-cache-dir install -r requirements.txt

# # Set the command to run the Flask application
# CMD ["flask", "run", "--host=0.0.0.0", "--port=8046"]

# FROM python:3-alpine3.15
FROM --platform=linux/amd64 python:3-alpine3.15

# RUN apk update && \
#     apk add py3-pip python3-dev

WORKDIR /app
COPY . /app/project
COPY execute_db.py /app

# Create a virtual environment
# RUN python3 -m venv venv

# Activate the virtual environment
# RUN source venv/bin/activate

# Install dependencies within the virtual environment
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt
RUN pip install -r project/requirements.txt
RUN python3 execute_db.py
EXPOSE 8046
# RUN chmod +x venv/bin/flask
# Set the command to run the Flask application
ENV FLASK_APP=project
ENV FLASK_DEBUG=1
CMD ["flask", "run", "--host=0.0.0.0", "--port=8046"]
