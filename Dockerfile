FROM centos:7

LABEL maintainer "srtabs@gmail.com"

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install python-devel
RUN yum -y install python-pip
RUN yum -y install python34
RUN yum -y install python34-devel
RUN yum -y install gcc-c++
RUN yum -y install gettext
RUN yum -y install npm
RUN yum -y install git

# install bower
RUN npm install --global bower

# Disable Python Output Buffer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH $PYTHONPATH:/app/alexandria_docs
ENV TERM=linux

# Create app directory
RUN mkdir /app
WORKDIR /app

# Add all files [Except the ones in dockerignore file]
COPY . /app/

RUN chmod +x /app/docker/docker-entrypoint.sh

# update pip and setuptools
RUN pip install pip setuptools --upgrade
# install project dependencies
RUN pip install -r requirements/docker.txt --upgrade

EXPOSE 8000

ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
