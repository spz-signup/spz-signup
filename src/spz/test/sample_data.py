# -*- coding: utf-8 -*-

"""Provides list which can be used for (pseudo) random sample data generation.
"""

import random

from spz.models import Origin, Degree, Applicant

first_names = ["Alexandra", "Ben", "Carla", "Dan", "Emily", "Finn", "Greta", "Hans", "Ida", "Jan"]

last_names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Schäfer", "Meyer", "Wagner", "Becker", "Bauer"]

mail_providers = ['gmail.com', 'outlook.com', 'yahoo.com', 'gmx.de', 'web.de']


def make_applicant(id=0):
    tag = "{}".format(10000 + id)
    mail = "{}@mail.com".format(tag)
    random.seed(id)
    return Applicant(
        mail=mail,
        tag=tag,
        first_name=random.choice(first_names),
        last_name=random.choice(last_names),
        phone="0157 {:5}".format(random.randint(0, 99999)),
        semester=random.randint(1, 26),
        origin=random.choice(Origin.query.all()),
        degree=random.choice(Degree.query.all())
    )
