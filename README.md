SPZ Signup
==========

<table>
<tr>
    <td>Authors</td>
    <td>
        Roman Zukowsky (roman@zukowsky.de)<br>
        Daniel Hofmann (daniel+spz@trvx.org)<br>
        Marco Neumann (marco@crepererum.net)<br>
        Felix Rittler (felix.rittler@web.de)<br>
        Tobias Dierich (spz@tobiasdierich.de)<br>
        Simon Zimmermann (timzi777@gmail.com)<br>
        Jan Fenker (coding@fenker.eu)<br>
    </td>
</tr>
<tr>
    <td>Organization</td>
    <td>Sprachenzentrum KIT Karlsruhe</td>
</tr>
<tr>
    <td>Source</td>
    <td>https://github.com/spz-signup/spz-signup</td>
</tr>
</table>


# About
Sign up management for the language courses at the KIT Sprachenzentrum.

Feel free to report issues to our [issue tracker](https://github.com/spz-signup/spz-signup/issues).


# Project Structure
This repository contains the [Docker Compose](https://docs.docker.com/compose/) files for running our SPZ Signup Managment application.
The application consists of several "Images", of which each one fullfills a different function.

## Components

### App
The [WSGI](https://www.python.org/dev/peps/pep-3333/)-app makes up the main component of our project:
It contains the user interfaces and the actual logic for the Signup Management.
The apps source code is contained in a separate repository at https://github.com/spz-signup/spz-signup-app.

### Database
The app stores its persistent data in a database.
Currently we use [PostgreSQL](https://www.postgresql.org/about/) but other database implementations could be used too (with small alterations to the underlying data model).

### Webserver
Although the app uses uWSGI, which is already a fully-featured web server, we use [NGINX](https://docs.nginx.com/) as a proxy for improved performance and security.
To simplify the amount of neccessary configuration (especially for LetsEncrypt) we prefer the image [nginx-proxy](https://hub.docker.com/r/jwilder/nginx-proxy) by jwilder over an official nginx build.

### Celery + Redis
In the current implmentation we use [Celery](https://docs.celeryproject.org/en/stable/) for several periodic tasks (e.g. Ilias-harvesting).
This setup requires quite a few docker images:
* Celery Beat
* Celery Workers (default and slow_mails)
* Redis (which is used for inter process communication)

### Mail
We use [OpenSMPTD](https://www.opensmtpd.org/) for delivering confirmation mails (and alike) to course applicants and participants.
During development we do not send out actual emails but use the image [maildev](https://hub.docker.com/r/maildev/maildev).

### Production-only Components
For production we also use the docker images [jrcs/letsencrypt-nginx-proxy-companion](https://hub.docker.com/jrcs/letsencrypt-nginx-proxy-companion), [spzsignup/docker-postgres-backup](https://hub.docker.com/spzsignup/docker-postgres-backup) and [southclaws/restic-robot](https://hub.docker.com/southclaws/restic-robot).
