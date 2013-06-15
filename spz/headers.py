# -*- coding: utf-8 -*-

"""User-protecting headers.

   .. warning::
      The webserver we deploy this application on should take care of the headers.
"""

from functools import update_wrapper

from flask import make_response


def upheaders(f):
    """Updates the response with user-protecting headers.

       Provided headers:
         * X-Frame-Options
         * X-Content-Type-Options
         * X-Download-Options
         * X-XSS-Protection

      .. seealso:: https://www.owasp.org/index.php/List_of_useful_HTTP_headers
    """
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))

        resp.headers['X-Frame-Options'] = 'deny'
        resp.headers['X-Content-Type-Options'] = 'nosniff'
        resp.headers['X-Download-Options'] = 'noopen'
        resp.headers['X-XSS-Protection'] = '1; mode=block'

        return resp
    return update_wrapper(new_func, f)


# vim: set tabstop=4 shiftwidth=4 expandtab:
