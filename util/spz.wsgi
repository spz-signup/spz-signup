# This files is only needed for deploying the project with
# Apache's mod_wsgi. You do not need it while developing.

# For configuring Apache, see:
# http://flask.pocoo.org/docs/deploying/mod_wsgi/#configuring-apache

# If you're using a virtualenv, see:
# http://flask.pocoo.org/docs/deploying/mod_wsgi/#working-with-virtual-environments

# import sys
#
# activate_this = '/path/to/env/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
# sys.path.insert(0, '/path/to/application')


from spz import app as application


# vim: set tabstop=4 shiftwidth=4 expandtab:
