# AlexandriaDocs

[![Build Status](https://travis-ci.org/srtab/alexandriadocs.svg?branch=master)](https://travis-ci.org/srtab/alexandriadocs)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f3ff11fbcbdd4ef1ade40d8033e7642f)](https://www.codacy.com/app/srtabs/alexandriadocs?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=srtab/alexandriadocs&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/srtab/alexandriadocs/badge.svg?branch=master)](https://coveralls.io/github/srtab/alexandriadocs?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/srtab/alexandriadocs?branch=master)](https://bettercodehub.com/)

Allows you to host, group, and easily search all you documentation. It supports static site generators like Sphinx, MkDocs, Jekyll, Hugo, ... and many [others](https://www.staticgen.com/). You can use your favorite continuous integration tool to generate and send new versions through the available API JSON, or you can just do it manually.

AlexandriaDocs is built with Django 1.11 and supports Python 3.4, 3.5 and 3.6.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* [Docker](https://docs.docker.com/engine/installation/);
* [Docker Compose](https://docs.docker.com/compose/install/).

### Installing
Start by cloning the project to your local machine:
```shell
$ git clone https://github.com/srtab/alexandriadocs
```

Enter on the cloned folder and start `docker-compose` with build flag:
```shell
$ cd alexandriadocs
$ docker-compose up --build
```

After the build finished, go to `http://127.0.0.1:8000`.

## Running the tests
You need to enter in the `app` container to execute the tests:
```shell
$ docker-compose exec app bash
```

### Unit tests
We use `tox` to execute our tests and its configured to run in `python34`, `python35` and `python36`. For now, `app` image only have `python34` installed. The others versions are used to run on TravisCI.

Finally, to run the unit tests in our local machines:
```shell
$ tox -e py34
```

### And coding style tests
For code styling tests we use `flake8`:
```
$ tox -e flake8
```

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/srtab/alexandriadocs/tags).

## Authors
* **Sandro Rodrigues** - *Initial work* - [srtab](https://github.com/srtab)

See also the list of [contributors](https://github.com/srtab/alexandriadocs/contributors) who participated in this project.

## License
This project is licensed under the Apache-2.0 - see the [LICENSE.md](LICENSE.md) file for details.
