# -*- coding: utf-8 -*-

"""The application's models.

   Manages the mapping between abstract entities and concrete database models.
"""

from datetime import datetime

from spz import db


# Ressources:
# http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html#sqlalchemy.schema.Column
# http://docs.sqlalchemy.org/en/rel_0_8/core/types.html
# http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html

class Attendance(db.Model):
    """Associates an :py:class:`Applicant` to a :py:class:`Course`.

       :param course: The :py:class:`Course` an :py:class:`Applicant` attends.
       :param status: The :py:class:`StateOfAtt` of the :py:`Attendance`.
       :param graduation: The intended :py:class:`Graduation` of the :py:`Attendance`.

       .. seealso:: the :py:data:`Applicant` member functions for an easy way of establishing associations
    """

    __tablename__ = 'attendance'

    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    course = db.relationship("Course", backref="applicant_attendances")

    status_id = db.Column(db.Integer, db.ForeignKey('stateofatt.id'))
    status = db.relationship("StateOfAtt", backref="attendances")

    graduation_id = db.Column(db.Integer, db.ForeignKey('graduation.id'))
    graduation = db.relationship("Graduation", backref="attendances")

    registered = db.Column(db.DateTime())

    def __init__(self, course, status, graduation, registered=datetime.utcnow()):
        self.course = course
        self.status = status
        self.graduation = graduation
        self.registered = registered

    def __repr__(self):
        return '<Attendance %r %r %r>' % (self.applicant, self.course, self.status)


class Applicant(db.Model):
    """Represents a person, applying for one or more :py:class:`Course`.

       Use the :py:func:`add_course_attendance` and :py:func:`remove_course_attendance`
       member functions to associate a :py:class:`Applicant` to a specific :py:class:`Course`.

       :param mail: Mail address
       :param tag: System wide identification tag
       :param sex: Male or not male
       :param first_name: First name
       :param last_name: Last name
       :param phone: Optional phone number
       :param degree: Degree aimed for
       :param semester: Enrolled in semester
       :param origin: Facility of origin
       :param registered: When this user was registered **in UTC**; defaults to utcnow()

       .. seealso:: the :py:data:`Attendance` association
    """

    __tablename__ = 'applicant'

    id = db.Column(db.Integer, primary_key=True)

    mail = db.Column(db.String(120), unique=True, nullable=False)
    tag = db.Column(db.String(10), unique=True)

    sex = db.Column(db.Boolean)

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20))

    degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'))
    degree = db.relationship("Degree", backref="applicants")

    semester = db.Column(db.Integer)

    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))
    origin = db.relationship("Origin", backref="applicants")

    # See {add,remove}_course_attendance member functions below
    course = db.relationship("Attendance", backref="applicant", cascade='all, delete-orphan')

    registered = db.Column(db.DateTime())

    def __init__(self, mail, tag, sex, first_name, last_name, phone, degree, semester, origin, registered=datetime.utcnow()):
        self.mail = mail
        self.tag = tag
        self.sex = sex
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.degree = degree
        self.semester = semester
        self.origin = origin
        self.registered = registered

    def __repr__(self):
        return '<Applicant %r %r>' % (self.mail, self.tag)

    def add_course_attendance(self, course, status, graduation):
        attendance = Attendance(course, status, graduation)
        self.course.append(attendance)

    def remove_course_attendance(self, course):
        self.course = filter(lambda attendance: attendance.course != course, self.course)

    def is_student(self):
        registered = Registration.query.filter_by(rnumber=self.tag).first()
        return True if registered else False

    def best_english_result(self):
        results = [app.percent for app in Approval.query.filter_by(tag=self.tag).all()]
        best = max(results) if results else 0
        return best


class Course(db.Model):
    """Represents a course that has a :py:class:`Language` and gets attended by multiple :py:class:`Applicant`.

       :param level: The course's level
       :param limit: The max. number of :py:class:`Applicant` that can attend this course.
       :param price: The course's price.
       :param language: The :py:class:`Language` for this course

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'course'
    __table_args__ = (db.UniqueConstraint('language_id', 'level'),)

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    level = db.Column(db.String(20))
    limit = db.Column(db.Integer, db.CheckConstraint('"limit" > 0'), nullable=False)  # limit is SQL keyword
    price = db.Column(db.Integer, db.CheckConstraint('price > 0'), nullable=False)

    def __init__(self, language, level, limit, price):
        self.language = language
        self.level = level
        self.limit = limit
        self.price = price

    def __repr__(self):
        return '<Course %r %r>' % (self.language, self.level)


class Language(db.Model):
    """Represents a language for a :py:class:`course`.

       :param name: The language's name
       :param signup_begin: The date time the signup begins **in UTC**
       :param signup_end: The date time the signup ends **in UTC**; constraint to **end > begin**
    """

    __tablename__ = 'language'
    __table_args__ = (db.CheckConstraint('signup_end > signup_begin'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    courses = db.relationship('Course', backref='language', lazy='dynamic')

    # Not using db.Interval here, because it needs native db support
    # See: http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#sqlalchemy.types.Interval
    signup_begin = db.Column(db.DateTime())
    signup_end = db.Column(db.DateTime())

    def __init__(self, name, signup_begin, signup_end):
        self.name = name
        self.signup_begin = signup_begin
        self.signup_end = signup_end

    def __repr__(self):
        return '<Language %r>' % self.name


class Degree(db.Model):
    """Represents the degree a :py:class:`Applicant` aims for.

       :param name: The degree's name
    """

    __tablename__ = 'degree'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Degree %r>' % self.name


class Graduation(db.Model):
    """Represents the graduation a :py:class:`Applicant` aims for.

       :param name: The graduation's name
    """

    __tablename__ = 'graduation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Graduation %r>' % self.name


class StateOfAtt(db.Model):
    """Represents the state of attendance a :py:class:`Applicant` aims for.

       :param name: The state's name
    """

    __tablename__ = 'stateofatt'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<StateOfAtt %r>' % self.name


class Origin(db.Model):
    """Represents the origin of a :py:class:`Applicant`.

       :param name: The origin's name
    """

    __tablename__ = 'origin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Origin %r>' % self.name


class Registration(db.Model):
    """Represents the registration a :py:class:`Applicant` aims for.

       :param rnumber: The registration number
    """

    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True)
    rnumber = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, rnumber):
        self.rnumber = rnumber

    def __eq__(self, other):
        return self.rnumber == other.rnumber

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return '<Registration %r>' % self.rnumber


class Approval(db.Model):
    """Represents the approval for English cours a :py:class:`Applicant` aims for.

       :param tag: The registration number or other identification
       :param percent: applicant's level for English course
    """

    __tablename__ = 'approval'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), nullable=False)  # tag may be not unique, multiple tests taken
    percent = db.Column(db.Integer, nullable=False)

    def __init__(self, tag, percent):
        self.tag = tag
        self.percent = percent

    def __repr__(self):
        return '<Approval %r %r>' % (self.tag, self.percent)


# vim: set tabstop=4 shiftwidth=4 expandtab:
