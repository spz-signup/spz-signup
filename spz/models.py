# -*- coding: utf-8 -*-

"""The application's models.

   Manages the mapping between abstract entities and concrete database models.
"""

from datetime import datetime

from sqlalchemy import func

from spz import app, db


# Ressources:
# http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html#sqlalchemy.schema.Column
# http://docs.sqlalchemy.org/en/rel_0_8/core/types.html
# http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html

class Attendance(db.Model):
    """Associates an :py:class:`Applicant` to a :py:class:`Course`.

       :param course: The :py:class:`Course` an :py:class:`Applicant` attends.
       :param graduation: The intended :py:class:`Graduation` of the :py:`Attendance`.
       :param waiting: Represents the waiting status of this :py:class`Attendance`.
       :param has_to_pay: Represents if this :py:class:`Attendance` was already payed for.

       .. seealso:: the :py:data:`Applicant` member functions for an easy way of establishing associations
    """

    __tablename__ = 'attendance'

    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    course = db.relationship("Course", backref="attendances")

    graduation_id = db.Column(db.Integer, db.ForeignKey('graduation.id'))
    graduation = db.relationship("Graduation", backref="attendances")

    waiting = db.Column(db.Boolean)
    has_to_pay = db.Column(db.Boolean)
    discounted = db.Column(db.Boolean)
    paidbycash = db.Column(db.Boolean)
    amountpaid = db.Column(db.Integer, db.CheckConstraint('amountpaid >= 0'), nullable=False)

    registered = db.Column(db.DateTime())
    payingdate = db.Column(db.DateTime())

    def __init__(self, course, graduation, waiting, has_to_pay, registered=None):
        self.course = course
        self.graduation = graduation
        self.waiting = waiting
        self.has_to_pay = has_to_pay
        self.discounted = False
        self.paidbycash = False
        self.amountpaid = 0
        self.registered = datetime.utcnow()
        self.payingdate = None

    def __repr__(self):
        return '<Attendance %r %r>' % (self.applicant, self.course)


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
    tag = db.Column(db.String(10), unique=False, nullable=True)  # XXX

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
    attendances = db.relationship("Attendance", backref="applicant", cascade='all, delete-orphan')

    registered = db.Column(db.DateTime())

    def __init__(self, mail, tag, sex, first_name, last_name, phone, degree, semester, origin, registered=None):
        self.mail = mail
        self.tag = tag
        self.sex = sex
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.degree = degree
        self.semester = semester
        self.origin = origin
        self.registered = datetime.utcnow()

    def __repr__(self):
        return '<Applicant %r %r>' % (self.mail, self.tag)

    def add_course_attendance(self, *args, **kwargs):
        attendance = Attendance(*args, **kwargs)
        self.attendances.append(attendance)

    def remove_course_attendance(self, course):
        self.attendances = filter(lambda attendance: attendance.course != course, self.attendances)

    def is_student(self):
        registered = Registration.query.filter(func.lower(Registration.number) == func.lower(self.tag)).first()
        return True if registered else False

    def best_rating(self):
        results = [approval.percent for approval in Approval.query.filter(func.lower(Approval.tag) == func.lower(self.tag)).all()]
        best = max(results) if results else 0
        return best

    def has_to_pay(self):
        attends = len(filter(lambda attendance: not attendance.waiting, self.attendances))
        return not self.is_student() or attends > 0

    def in_course(self, course):
        return course in [attendance.course for attendance in self.attendances]


class Course(db.Model):
    """Represents a course that has a :py:class:`Language` and gets attended by multiple :py:class:`Applicant`.

       :param language: The :py:class:`Language` for this course
       :param level: The course's level
       :param limit: The max. number of :py:class:`Applicant` that can attend this course.
       :param price: The course's price.
       :param rating_highest: The course's upper bound of required rating.
       :param rating_lowest: The course's lower bound of required rating.

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'course'
    __table_args__ = (db.UniqueConstraint('language_id', 'level'),
                      db.CheckConstraint('rating_highest >= rating_lowest'))

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    level = db.Column(db.String(120))
    limit = db.Column(db.Integer, db.CheckConstraint('"limit" > 0'), nullable=False)  # limit is SQL keyword
    price = db.Column(db.Integer, db.CheckConstraint('price > 0'), nullable=False)

    rating_highest = db.Column(db.Integer, db.CheckConstraint('rating_highest >= 0'), nullable=False)
    rating_lowest = db.Column(db.Integer, db.CheckConstraint('rating_lowest >= 0'), nullable=False)

    def __init__(self, language, level, limit, price, rating_highest, rating_lowest):
        self.language = language
        self.level = level
        self.limit = limit
        self.price = price
        self.rating_highest = rating_highest
        self.rating_lowest = rating_lowest

    def __repr__(self):
        return '<Course %r %r>' % (self.language, self.level)

    def is_allowed(self, applicant):
        return self.rating_lowest <= applicant.best_rating() <= self.rating_highest

    def is_full(self):
        return len(self.get_active_attendances()) >= self.limit

    def is_overbooked(self):
        return len(self.attendances) >= (self.limit * app.config['OVERBOOKING_FACTOR'])

    def get_waiting_attendances(self):
        return filter(lambda attendance: attendance.waiting, self.attendances)

    def get_active_attendances(self):
        return filter(lambda attendance: not attendance.waiting, self.attendances)

    def get_paying_attendances(self):
        return filter(lambda attendance: not attendance.waiting and attendance.has_to_pay, self.attendances)

    def get_free_attendances(self):
        return filter(lambda attendance: not attendance.waiting and not attendance.has_to_pay, self.attendances)

    def restock(self):
        # Negative number of free seats may happen if s.o. manually added an attendance
        num_free = max(self.limit - len(self.get_active_attendances()), 0)
        waiting = self.get_waiting_attendances()

        to_move = waiting[:num_free]

        # Check if an applicant has to pay before toggling the waiting status,
        # otherwise he has to pay _from the status change_ on.
        for attendance in to_move:
            attendance.has_to_pay = attendance.applicant.has_to_pay()
            attendance.waiting = False

        return to_move


class Language(db.Model):
    """Represents a language for a :py:class:`course`.

       :param name: The language's name
       :param signup_begin: The date time the signup begins **in UTC**
       :param signup_end: The date time the signup ends **in UTC**; constraint to **end > begin**
    """

    __tablename__ = 'language'
    __table_args__ = (db.CheckConstraint('signup_end > signup_begin'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    reply_to = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', backref='language', lazy='dynamic')

    # Not using db.Interval here, because it needs native db support
    # See: http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#sqlalchemy.types.Interval
    signup_begin = db.Column(db.DateTime())
    signup_end = db.Column(db.DateTime())

    def __init__(self, name, reply_to, signup_begin, signup_end):
        self.name = name
        self.reply_to = reply_to
        self.signup_begin = signup_begin
        self.signup_end = signup_end

    def __repr__(self):
        return '<Language %r>' % self.name

    def is_open_for_signup(self):
        now = datetime.utcnow()
        return self.signup_begin < now < self.signup_end


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
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Graduation %r>' % self.name


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
    """Registration number for a :py:class:`Applicant` that is a student.

       :param number: The registration number
    """

    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, number):
        self.number = number

    def __eq__(self, other):
        return self.number == other.number

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return '<Registration %r>' % self.number


# XXX: This should hole a ref to the specific language the rating is for
#      it's ok as of now, because we only got english test results.
class Approval(db.Model):
    """Represents the approval for English courses a :py:class:`Applicant` aims for.

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
