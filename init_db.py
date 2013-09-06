# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import json
from jsonschema import validate, ValidationError, SchemaError

from spz import app, db
from spz.models import *  # Keep this import, otherwise the create_all call won't any models at all


def validate_resources():
    resources = ('degrees', 'origins', 'courses', 'sexes')

    for fname in resources:
        with app.open_resource('resource/{0}.json'.format(fname)) as fd_json, app.open_resource('resource/{0}.schema'.format(fname)) as fd_schema:
            res_json = json.load(fd_json)
            res_schema = json.load(fd_schema)

            validate(res_json, res_schema)


def insert_resources():
    with app.open_resource('resource/sexes.json') as fd:
        res = json.load(fd)

        for sex in res["sexes"]:
            db.session.add(Sex(sex))

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
            db.session.add(Origin(origin))

    with app.open_resource('resource/courses.json') as fd:
        res = json.load(fd)

        for language in res["languages"]:
            ref_lang = Language(language["name"], datetime.utcnow(), datetime.utcnow() + timedelta(weeks=2))

            for course in language["courses"]:
                db.session.add(Course(ref_lang, course["level"], limit=20, price=60))

    db.session.commit()


# Has to be done only once, to initialize the database;
# do not use this in regular code

if __name__ == '__main__':
    try:
        validate_resources()  # Strong exception safety guarantee

        db.create_all()
        insert_resources()

        print('Import OK')
    except (ValidationError, SchemaError) as e:
        print(e)  # Stacktrace does not contain any useful information


# vim: set tabstop=4 shiftwidth=4 expandtab:
