[![black][black-shield]][black-url]
[![Python][python-shield]][python-url]
[![Django][django-shield]][django-url]
[![Docker][docker-shield]][docker-url]
[![License][license-shield]][license-url]

# MyVehicles

MyVehicles is a self-hosted vehicle expense tracking solution to all of your vehicles.

# Translation

**myvehicles** is currently available in English and French.

## Installation

### With Docker

Example for a NAS synology with 🐳 Docker.

Firstly, go to File Station and open the docker folder.
Inside the docker folder, create one new folder and name it `"myvehicles"`.
Follow the instructions in the image below.

Now create two new folders inside the `"myvehicles"` folder that you created
at STEP 3 and name one `"db"` and the other `"media"`.
Follow the instructions in the image below.

**Note:** Be careful to enter only lowercase, not uppercase letters.

```sh
docker -run -d  --name=myvehicles \
-p 8765:8765 \
-v "/volume1/docker/myvehicles/media:/app/media" \
-v "/volume1/docker/myvehicles/db:/app/db" \
--restart always \
hvincent05/myvehicles
```

### or with Docker-Compose

```yaml
version: "3.7"
services:
  web:
    container_name: myvehicles
    image: hvincent05/myvehicles
    restart: always
    environment:
      MESVEHICULES_URL: "http://localhost:8765"
    volumes:
      - /volume1/docker/myvehicles/media:/app/media
      - /volume1/docker/myvehicles/db:/app/db
    ports:
      - "8765:8765"
```

```sh
docker-compose up -d
```

## Build with

- Python 3.9
- Django 4.1
- django-private-storage
- Pillow 9.2.0
- python-dotenv
- bootstrap 5
- chart.js

---

[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[python-shield]: https://img.shields.io/badge/Python-3.9-blue
[python-url]: https://www.python.org/downloads/
[django-shield]: https://img.shields.io/badge/Django-4.1-brightgreen
[django-url]: https://www.djangoproject.com
[docker-shield]: https://img.shields.io/badge/Docker-20.10-blue
[docker-url]: https://www.docker.com
[license-shield]: https://img.shields.io/github/license/vincenthouillon/myvehicles.svg
[license-url]: https://github.com/vincenthouillon/myvehicles/blob/master/LICENSE
