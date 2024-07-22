FROM mcr.microsoft.com/devcontainers/python:3.8

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get -y install --no-install-recommends postgresql-client \
	&& apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install tensorflow tensorflowjs keras flask psycopg[binary] gunicorn
RUN pip install notebook

WORKDIR /home/vscode

EXPOSE 5000
EXPOSE 8888

CMD ["./entrypoint.sh"]
