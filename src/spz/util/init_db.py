#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from uuid import uuid4

from flask import json
from jsonschema import validate, ValidationError, SchemaError

from spz import app, db
from spz.models import *  # Keep this import, otherwise the create_all call won't any models at all


def validate_resources():
    resources = ('degrees', 'origins', 'courses', 'degrees', 'graduations', 'users')

    for fname in resources:
        with app.open_resource('resource/{0}.json'.format(fname)) as fd_json, \
             app.open_resource('resource/{0}.schema'.format(fname)) as fd_schema:

            res_json = json.load(fd_json)
            res_schema = json.load(fd_schema)

            validate(res_json, res_schema)


def insert_resources():
    with app.open_resource('resource/degrees.json') as fd:
        res = json.load(fd)

        for degree in res["degrees"]:
            db.session.add(Degree(degree))

    with app.open_resource('resource/graduations.json') as fd:
        res = json.load(fd)

        for graduation in res["graduations"]:
            db.session.add(Graduation(graduation))

    with app.open_resource('resource/origins.json') as fd:
        res = json.load(fd)

        for origin in res["origins"]:
            db.session.add(Origin(
                name=origin["name"],
                validate_registration=origin["validate_registration"]
            ))

    with app.open_resource('resource/courses.json') as fd:
        res = json.load(fd)

        for language in res["languages"]:
            ref_lang = Language(
                language["name"],
                language["reply_to"],
                datetime.strptime(language["signup_begin_iso_utc"], "%Y-%m-%dT%H:%M:%SZ"),  # ISO 8601 / RFC 3339 -- better way to parse this?
                datetime.strptime(language["signup_random_window_end_iso_utc"], "%Y-%m-%dT%H:%M:%SZ"),
                datetime.strptime(language["signup_end_iso_utc"], "%Y-%m-%dT%H:%M:%SZ"),    # see also Jsonschema RFC, date-time
                datetime.strptime(language["signup_auto_end_iso_utc"], "%Y-%m-%dT%H:%M:%SZ")
            )

            for course in language["courses"]:
                for alt in course["alternative"]:
                    db.session.add(Course(
                        language=ref_lang,
                        level=course["level"],
                        alternative=alt,
                        limit=course["limit"],
                        price=course["price"],
                        rating_lowest=course["rating_lowest"],
                        rating_highest=course["rating_highest"],
                        collision=course["collision"]
                    ))

    db.session.commit()

    with app.open_resource('resource/users.json') as fd:
        res = json.load(fd)

        print("create user accounts:")
        for user in res["users"]:
            ref_langs = []
            for lang_name in user["languages"]:
                lang = Language.query.filter(Language.name == lang_name).first()
                if lang:
                    ref_langs.append(lang)
                else:
                    print("  WARNING: language {} does not exist (user={})".format(lang_name, user["email"]))
            u = User(
                email=user["email"],
                active=user["active"],
                superuser=user["superuser"],
                languages=ref_langs
            )
            pw = u.reset_password()
            print('  {} : {}'.format(u.email, pw))
            db.session.add(u)

    db.session.commit()


# Has to be done only once, to initialize the database;
# do not use this in regular code

if __name__ == '__main__':
    try:
        validate_resources()  # Strong exception safety guarantee
    except (ValidationError, SchemaError) as e:
        print(e)  # Stacktrace does not contain any useful information
        sys.exit()

    # Request polite confirmation
    token = uuid4().hex[:5]  # repeat random token of arbitrary length
    # OK, not an interactive process, try something else
    if 'YES_I_KNOW_THAT_WORLD_ENDS_NOW' in os.environ:
        user_in = token
    else:
        user_in = input('Create and drop tables using {0}\nConfirm by repeating the following token\n{1}\n'.format(db, token))

    if token == user_in:
        db.drop_all()
        db.create_all()
        insert_resources()

        print('Import OK.')
    else:
        print('Aborting: {0} did not match token {1}'.format(user_in, token))
