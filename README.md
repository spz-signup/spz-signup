SPZ Signup
==========

| Authors | Roman Zukowsky <roman@zukowsky.de> <br>
          - Daniel Hofmann <daniel+spz@trvx.org> <br>
          - Marco Neumann <marco@crepererum.net> <br>
          - Felix Rittler <felix.rittler@web.de> <br>
          - Tobias Dierich <spz@tobiasdierich.de> <br>
          - Simon Zimmermann <timzi777@gmail.com> <br> |
| Organization | Sprachenzentrum KIT Karlsruhe |
| Source | https://github.com/spz-signup/spz-signup |

# About
Sign up management for the language courses at the KIT Sprachenzentrum.

Feel free to report issues to our `issue tracker`_.


# Project Structure
This repository contains the `Docker Compose`_ files for running our SPZ Signup Managment application.
The application consists of several "Images", of which each one fullfills a different function.

## Components

### App
The `WSGI`-app makes up the main component of our project:
It contains the user interfaces and the actual logic for the Signup Management.
The apps source code is contained in a separate repository at https://github.com/spz-signup/spz-signup-app.

### Database
The app stores its persistent data in a database.
Currently we use `PostgreSQL`_ but other database implementations could be used too (with small alterations to the underlying data model).

### Webserver
Although the app uses uWSGI, which is already a fully-featured web server, we use `NGINX`_ as a proxy for improved performance and security.
To simplify the amount of neccessary configuration (especially for LetsEncrypt) we prefer the image `nginx-proxy`_ by jwilder over an official nginx build.

### Celery + Redis
In the current implmentation we use `Celery`_ for several periodic tasks (e.g. Ilias-harvesting).
This setup requires quite a few docker images:
* Celery Beat
* Celery Workers (default and slow_mails)
* Redis (which is used for inter process communication)

### Mail
We use `OpenSMPTD`_ for delivering confirmation mails (and alike) to course applicants and participants.
During development we do not send out actual emails but use the image `maildev`_.

### Production-only Components
For production we also use the docker images `jrcs/letsencrypt-nginx-proxy-companion`, `spzsignup/docker-postgres-backup` and `southclaws/restic-robot`.


.. _issue tracker: https://github.com/spz-signup/spz-signup/issues
.. _Docker Compose: https://docs.docker.com/compose/
.. _WSGI: https://www.python.org/dev/peps/pep-3333/
.. _PostgreSQL: https://www.postgresql.org/about/
.. _NGINX: https://docs.nginx.com/
.. _nginx-proxy: https://hub.docker.com/r/jwilder/nginx-proxy
.. _Celery: https://docs.celeryproject.org/en/stable/
.. _OpenSMPTD: https://www.opensmtpd.org/
.. _maildev: https://hub.docker.com/r/maildev/maildev
