# Deployment
This document explains how to deploy the system. This has to be done before the sign-up for the intensive courses starts. We'll wipe everything, so you don't have to worry about (database) migration.

## 0. 1-Month ahead Checklist
Please follow that checklist approximately 1 month ahead to ensure that we have all external requirements:
- TLS certificate up-to-date? (at least 10 months remaining)
- Ilias user still valid and active?
- English test created?
- make Ilias user admin of the course that contains the English test
- ensure that we get a fresh list of matriculation IDs
- ask SPZ leader for new course list (**WARNING: time is UTC!**)
- recheck all timings, also with the English department (`RANDOM_PERIOD` and friends as well as celery scheduler)
- ensure that python requirements and assets are up-to-date
- consider upgrading base image versions for Docker

## 1. Preparation
Before you can start with the actual deployment process, there is some formal work to do.

### 1.1 Backup
Make a DB backup from the old data!

### 1.2 GIT
- add a tag `release-YYYY.MM.DD.COUNTER` (`COUNTER` starts at 0), so we can reload DB dumps later (we don't develop DB update scripts) and check what behaviour changed over the last semester. use `git tag -a ...` and `git push origin --tags`

### 1.3 Host System
- update
- ensure sane Docker config (logging to journald, IPv6)
- that's a good moment to do a reboot

## 2. Images and Docker

### 2.1 nginx
- change `serve_name` from `localhost` to `anmeldung.spz.kit.edu` (twice!)
- regenerate DH params: `openssl dhparam -outform PEM -out dhparam.pem 4096`
- set correct key to `main.key.pem`
- set cert + chain to `main.crt+chain.pem`: 1. our cert, 2.... all intermediate certs, starting with the "nearest" one going up to the root CA, **without** root CA (also called anchor)

### 2.2 postgres
*No changes required.*

### 2.3 redis
*No changes required.*

### 2.4 maildev
*Won't be used.*

### 2.5 mailprod
*No changes required.*

### 2.6 spz
That's our baby, requires a good amount of modifications. I'll walk you through all files and explain which changes are required.

`uwsgi.ini`:
- `python-autoreload = 1` => `python-autoreload = 0`


`instances/development.conf`:
- `DEBUG = True` => `DEBUG = False`
- set new DB password in `SQLALCHEMY_DATABASE_URI`
- generate 3 random entries for `SECRET_KEY`, `TOKEN_SECRET_KEY` and `ARGON2_SALT`
- set `SEMESTER_NAME` to the correct value
- enter `ILIAS_USERNAME`, `ILIAS_PASSWORD` and `ILIAS_REFID` (hints: it's the integer value in the URL of the test, not the one of the course that contains it)

`util/docker_entrypoint.sh`
- set correct DB password to the line `PGPASSWORD=mysecretpassword psql -h postgres ...` somewhere in the `init` function

### 2.7 compose file
- remove all `ports` entries, apart from the nginx ones where you just have to remove the `127.0.0.1:` prefix (two, port 80 and 443) of course
- replace `maildev` with `mailprod`, renable `read-only`. no need to adjust the volumes, they are designed to work with both
- set correct (new, but same as used for the `spz` image) to the `POSTGRES_PASSWORD` env variable of the `postgres` container
- remove `--autoreload` flag from `celery_default` and `celery_slow_mails` command entries
- remove relative image mounts (starting with `./images`) from `uwsgi` container

## 3. Fire it up
- ensure you're acting for the server docker and not your local one (you might want to use a SSH tunnel and the client TLS certificate)
- hopefully you have a backup at this point
- `docker-compose down -v` -- that wipes everything
- `docker-compose build --pull` -- ensures you get fresh upstream images during the build
- `docker-compose up -d` -- launch new containers
- `docker-compose logs` to get the generated login credentials for all users

## 4. Testing
Check if system is reachable from the outer world, login with your credentials, play around.

## 5. Final mail
After everything seems to be OK, send out mails to all users with their passwords. Wait for the sign-up day and hope that you didn't mess it up this time ;)

## 6. Aftermath and Fixes

### 6.1 Image Fixes or Upgrades
In case you have to do a hotfix or you want to update to the latest upstream images:
- `docker-compose build --pull`
- `docker-compose down` (**NO `-v` flag this time, otherwise you wipe everyting!**)
- `docker-compose up -d`

### 6.2 DB modifications
- `docker exec -it NAME_OF_THE_UWSGI_CONTAINER ipython`
- `import spz.models`
- do your changes
