FROM python:3.12.4-alpine

WORKDIR /usr/src/app

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure python output is sent directly to the terminal without buffering
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]