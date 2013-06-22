# -*- coding: utf-8 -*-

"""The application's models.

   Manages the mapping between abstract entities and concrete database models.
"""

from datetime import datetime

from spz import db


def init_db():
    """Creates all tables.

       .. warning:: Has to be done only once, to initialize the database; do not use this in regular code
    """
    db.create_all()


# TODO(daniel): check nullable constraints, string lengths, indices

# Ressources:
# http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html#sqlalchemy.schema.Column
# http://docs.sqlalchemy.org/en/rel_0_8/core/types.html
# http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html


# n:m, Applicants:Courses
attendances = db.Table(
    'attendances',
    db.Column('applicant_id', db.Integer, db.ForeignKey('applicant.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Applicant(db.Model):
    """Represents a person, applying for one or more :py:class:`Course`.

       :param mail: Mail address
       :param tag: System wide identification tag
       :param first_name: First name
       :param last_name: Last name
       :param phone: Optional phone number
       :param courses: A :py:class:`Applicant` attends one or multiple :py:class:`Course`
       :param degree: Degree aimed for
       :param semester: Enrolled in semester
       :param origin: Facility of origin
       :param registered: When this user was registered **in UTC**; defaults to utcnow()

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'applicant'

    id = db.Column(db.Integer, primary_key=True)

    mail = db.Column(db.String(120), unique=True, nullable=False)
    tag = db.Column(db.String(10), unique=True, nullable=False)

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20))

    courses = db.relationship("Course", secondary=attendances, backref="applicants")

    degree = db.relationship("Degree", uselist=False, backref="applicant")
    semester = db.relationship("Semester", uselist=False, backref="applicant")
    origin = db.relationship("Origin", uselist=False, backref="applicant")

    # TODO(daniel):
    registered = db.DateTime()

    def __init__(self, mail, tag, first_name, last_name, phone, courses, degree, semester, origin, registered=datetime.utcnow()):
        self.mail = mail
        self.tag = tag
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.courses = courses
        self.degree = degree
        self.semester = semester
        self.origin = origin
        self.registered = registered

    def __repr__(self):
        return '<Applicant %r>' % self.tag


class Course(db.Model):
    """Represents a course that has a :py:class:`Language` and gets attended by multiple :py:class:`Applicant`.

       :param level: The course's level
       :param limit: The max. number of :py:class:`Applicant` that can attend this course.
       :param price: The course's price.
       :param language: The :py:class:`Language` for this course

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))
    limit = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

    # TODO(daniel):
    # qualification eng

    def __init__(self, level, limit, price, language):
        self.level = level
        self.limit = limit
        self.price = price
        self.language = language

    def __repr__(self):
        return '<Course %r %r>' % (self.language, self.level)


class Language(db.Model):
    """Represents a language for a :py:class:`course`.

       :param name: The language's name
    """

    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    courses = db.relationship('Course', backref='language', lazy='dynamic')

    # TODO(daniel):
    # time interval, open for signup

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Language %r>' % self.name


class Degree(db.Model):
    """Represents the degree a :py:class:`Applicant` aims for.

       :param name: The degree's name
    """

    __tablename__ = 'degree'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Degree %r>' % self.name


class Semester(db.Model):
    """Represents the current semester a :py:class:`Applicant` is in.

       :param level: The semester's level
    """

    __tablename__ = 'semester'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))

    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return '<Semester %r>' % self.level


class Origin(db.Model):
    """Represents the origin of a :py:class:`Applicant`.

       :param name: The origin's name
    """

    __tablename__ = 'origin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'))
    department = db.relationship("Department", uselist=False, backref="origin")

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def __repr__(self):
        return '<Origin %r %r>' % (self.name, self.department)


class Department(db.Model):
    """Represents the department of a :py:class:`Origin` a :py:class:`Applicant` comes from.

       :param name: The department's name
    """

    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Department %r>' % self.name


# vim: set tabstop=4 shiftwidth=4 expandtab:
