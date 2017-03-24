FROM centos:7

RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install python-devel
RUN yum -y install python-pip
RUN yum -y install gcc-c++
RUN yum -y install gettext

# Disable Python Output Buffer
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH $PYTHONPATH:/app/alexandria_docs
ENV TERM=linux

# Create app directory
RUN mkdir /app
WORKDIR /app

# Add all files [Except the ones in dockerignore file]
ADD . /app/

# update pip and setuptools
RUN pip install pip setuptools --upgrade

# install project dependencies
RUN pip install -r requirements/docker.txt --upgrade

EXPOSE 8000

CMD ["python", "alexandria_docs/manage.py", "runserver", "0.0.0.0:8000"]