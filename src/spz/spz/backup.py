# -*- coding: utf-8 -*-

"""Automatic backup system.
"""

from datetime import datetime

import os

import subprocess

from flask_mail import Message

from spz import app, mail

from spz.util.Filetype import mime_from_filepointer


class BackupException(Exception):
    pass


def create():
    """Create a new full DB backup, compressed and encrypted."""
    now = datetime.utcnow()
    timestamp = now.strftime('%Y-%m-%d-%H-%M')
    fname = '/backup/backup-{}.sql.xz.enc'.format(timestamp)

    env = dict(
        os.environ,
        PGPASSWORD=app.config['DB_PW']
    )

    p = subprocess.Popen(
        ['/home/spz/code/util/backup.sh', fname],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    try:
        p.wait(100)
    except subprocess.TimeoutExpired:
        p.kill()
        stdout, stderr = p.communicate()
        raise BackupException(
            'timeout (stdout="{}", stderr="{}")'.format(stdout, stderr)
        )

    if p.returncode != 0:
        stdout, stderr = p.communicate()
        raise BackupException(
            'non-zero exit status (stdout="{}", stderr="{}")'.format(stdout, stderr)
        )


def is_backupfile(fname):
    """Check if given file name is a valid backup file.

       :param fname: file name w/o path
    """
    return fname.startswith('backup-') and fname.endswith('.sql.xz.enc')


def get_all_backups():
    """Returns a list of all backup files."""
    files_all = os.listdir('/backup')
    files_filtered = (
        fname
        for fname in files_all
        if is_backupfile(fname)
    )
    return [
        '/backup/{}'.format(fname)
        for fname in files_filtered
    ]


def send():
    """Send last backup to admins via email."""
    files = get_all_backups()
    if files:
        last = list(sorted(files, reverse=True))[0]
        with open(last, 'rb') as fp:
            msg = Message(
                sender=app.config['PRIMARY_MAIL'],
                recipients=app.config['ADMIN_MAILS'],
                subject='[Sprachenzentrum] Backup {}'.format(last),
                charset='utf-8'
            )
            mime = mime_from_filepointer(fp)
            data = fp.read()
            msg.attach(last, mime, data)
            mail.send(msg)
