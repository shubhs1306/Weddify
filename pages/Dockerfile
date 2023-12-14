# Base image with Python and dependencies
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /Weddify2/pages

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add freetype-dev freetype

# Copy the requirements file and install dependencies
RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . .

# Expose the port on which Django runs (default is 8000)
EXPOSE 8003

# Run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]
