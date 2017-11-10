FROM centos:7

LABEL maintainer "srtabs@gmail.com"

RUN yum -y update && yum -y install epel-release && \
    yum -y install python34-devel \
    python34-pip \
    gcc-c++ \
    gettext \
    npm \
    git

# install bower
RUN npm install --global bower

# Disable Python Output Buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH $PYTHONPATH:/app/alexandriadocs
ENV TERM=linux

# Create app directory
RUN mkdir /app
WORKDIR /app

# Add all files [Except the ones in dockerignore file]
COPY . /app/

RUN chmod +x /app/docker/docker-entrypoint.sh

# update pip and setuptools
RUN pip3.4 install pip setuptools --upgrade
# install project dependencies
RUN pip3.4 install -r requirements/docker.txt --upgrade

EXPOSE 8000

ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]

CMD ["python3.4", "manage.py", "runserver", "0.0.0.0:8000"]
