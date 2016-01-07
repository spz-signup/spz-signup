# -*- coding: utf-8 -*-

"""The application's models.

   Manages the mapping between abstract entities and concrete database models.
"""

from binascii import hexlify
from datetime import datetime
from functools import total_ordering
import random
import string

from argon2 import argon2_hash

from sqlalchemy import and_, between, func

from spz import app, db
import spz.models


# Ressources:
# http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html#sqlalchemy.schema.Column
# http://docs.sqlalchemy.org/en/rel_0_8/core/types.html
# http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html


def hash_secret(s):
    """Hash secret, case-sensitive string to binary data."""
    # WARNING: changing these parameter invalides the entire table!
    # INFO: buflen is in bytes, not bits! So this is a 256bit output
    #       which is higher than the current (2015-12) recommendation
    #       of 128bit. We use 2 lanes and 1MB of memory. One pass has
    #       to be enough, because otherwise we need to much time while
    #       importing.
    return argon2_hash(
        s.encode('utf8'),
        app.config['ARGON2_SALT'],
        buflen=32,
        t=1,
        p=2,
        m=(1 << 10)
    )


@total_ordering
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
    course = db.relationship("Course", backref="attendances", lazy="joined")

    graduation_id = db.Column(db.Integer, db.ForeignKey('graduation.id'))
    graduation = db.relationship("Graduation", backref="attendances", lazy="joined")

    waiting = db.Column(db.Boolean)
    has_to_pay = db.Column(db.Boolean)
    paidbycash = db.Column(db.Boolean)
    amountpaid = db.Column(db.Integer, nullable=False)

    registered = db.Column(db.DateTime(), default=datetime.utcnow)
    payingdate = db.Column(db.DateTime())

    amountpaid_constraint = db.CheckConstraint(amountpaid >= 0)

    def __init__(self, course, graduation, waiting, has_to_pay):
        self.course = course
        self.graduation = graduation
        self.waiting = waiting
        self.has_to_pay = has_to_pay
        self.paidbycash = False
        self.amountpaid = 0
        self.payingdate = None

    def __repr__(self):
        return '<Attendance %r %r>' % (self.applicant, self.course)

    def __lt__(self, other):
        return self.registered < other.registered


@total_ordering
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
    degree = db.relationship("Degree", backref="applicants", lazy="joined")

    semester = db.Column(db.Integer)  # TODO constraint: > 0, but still optional

    origin_id = db.Column(db.Integer, db.ForeignKey('origin.id'))
    origin = db.relationship("Origin", backref="applicants", lazy="joined")

    discounted = db.Column(db.Boolean)

    # See {add,remove}_course_attendance member functions below
    attendances = db.relationship("Attendance", backref="applicant", cascade='all, delete-orphan', lazy="joined")

    registered = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, mail, tag, sex, first_name, last_name, phone, degree, semester, origin):
        self.mail = mail
        self.tag = tag
        self.sex = sex
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.degree = degree
        self.semester = semester
        self.origin = origin
        self.discounted = False

    def __repr__(self):
        return '<Applicant %r %r>' % (self.mail, self.tag)

    def __lt__(self, other):
        return (self.last_name.lower(), self.first_name.lower()) < (other.last_name.lower(), other.first_name.lower())

    def add_course_attendance(self, *args, **kwargs):
        attendance = Attendance(*args, **kwargs)
        self.attendances.append(attendance)
        return attendance

    def remove_course_attendance(self, course):
        self.attendances = filter(lambda attendance: attendance.course != course, self.attendances)

    def is_student(self):
        return Registration.exists(self.tag)

    def best_rating(self):
        results = [approval.percent for approval in Approval.query.filter(func.lower(Approval.tag) == func.lower(self.tag))]
        best = max(results) if results else 0
        return best

    def has_to_pay(self):
        attends = len(filter(lambda attendance: not attendance.waiting, self.attendances))
        return not self.is_student() or attends > 0

    def in_course(self, course):
        return course in [attendance.course for attendance in self.attendances]

    def active_in_parallel_course(self, course):
        # do not include the course queried for
        active_in_courses = [attendance.course for attendance in self.attendances
                             if attendance.course != course and not attendance.waiting]

        active_parallel = filter(lambda crs: crs.language == course.language and crs.level == course.level,
                                 active_in_courses)

        return len(active_parallel) > 0

    # Management wants us to limit the global amount of attendances one is allowed to have.. so what can I do?
    def over_limit(self):
        now = datetime.utcnow()
        # at least do not count in courses that are already over..
        running = [att for att in self.attendances if att.course.language.signup_end >= now]
        return len(running) >= app.config['MAX_ATTENDANCES']


@total_ordering
class Course(db.Model):
    """Represents a course that has a :py:class:`Language` and gets attended by multiple :py:class:`Applicant`.

       :param language: The :py:class:`Language` for this course
       :param level: The course's level
       :param alternative: The course's alternative of the same level.
       :param limit: The max. number of :py:class:`Applicant` that can attend this course.
       :param price: The course's price.
       :param rating_highest: The course's upper bound of required rating.
       :param rating_lowest: The course's lower bound of required rating.

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    level = db.Column(db.String(120))
    alternative = db.Column(db.String(10), nullable=False)
    limit = db.Column(db.Integer, nullable=False)  # limit is SQL keyword
    price = db.Column(db.Integer, nullable=False)
    rating_highest = db.Column(db.Integer, nullable=False)
    rating_lowest = db.Column(db.Integer, nullable=False)

    unique_constraint = db.UniqueConstraint(language_id, level, alternative)
    limit_constraint = db.CheckConstraint(limit > 0)
    price_constraint = db.CheckConstraint(price > 0)
    rating_constraint = db.CheckConstraint(and_(
        between(rating_highest, 0, 100),
        between(rating_lowest, 0, 100),
        rating_lowest <= rating_highest
    ))

    def __init__(self, language, level, alternative, limit, price, rating_highest, rating_lowest):
        self.language = language
        self.level = level
        self.alternative = alternative
        self.limit = limit
        self.price = price
        self.rating_highest = rating_highest
        self.rating_lowest = rating_lowest

    def __repr__(self):
        return '<Course %r>' % (self.full_name())

    def __lt__(self, other):
        return (self.language, self.level.lower()) < (other.language, other.level.lower())

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

        # avoid restocking applicants already active in a parallel course
        waiting = filter(lambda attendance: not attendance.applicant.active_in_parallel_course(self), waiting)

        to_move = waiting[:num_free]

        # Check if an applicant has to pay before toggling the waiting status,
        # otherwise he has to pay _from the status change_ on.
        for attendance in to_move:
            attendance.has_to_pay = attendance.applicant.has_to_pay()
            attendance.waiting = False

        return to_move

    def full_name(self):
        return u'{0} {1} {2}'.format(self.language.name, self.level, self.alternative)


@total_ordering
class Language(db.Model):
    """Represents a language for a :py:class:`course`.

       :param name: The language's name
       :param signup_begin: The date time the signup begins **in UTC**
       :param signup_end: The date time the signup ends **in UTC**; constraint to **end > begin**
    """

    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    reply_to = db.Column(db.String(120), nullable=False)
    courses = db.relationship('Course', backref='language', lazy='joined')

    # Not using db.Interval here, because it needs native db support
    # See: http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#sqlalchemy.types.Interval
    signup_begin = db.Column(db.DateTime())
    signup_end = db.Column(db.DateTime())

    signup_constraint = db.CheckConstraint(signup_end > signup_begin)

    def __init__(self, name, reply_to, signup_begin, signup_end):
        self.name = name
        self.reply_to = reply_to
        self.signup_begin = signup_begin
        self.signup_end = signup_end

    def __repr__(self):
        return '<Language %r>' % self.name

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def is_open_for_signup_rnd(self, time):
        return self.signup_begin < time < (self.signup_begin + app.config['RANDOM_WINDOW_OPEN_FOR']) < self.signup_end

    def is_open_for_signup_fcfs(self, time):
        return (self.signup_begin + app.config['RANDOM_WINDOW_OPEN_FOR'] + app.config['RANDOM_WINDOW_CLOSED_FOR']) < time < self.signup_end

    def is_open_for_signup(self, time):
        # management wants the system to be: open a few hours, then closed "overnight" for random selection, then open again..
        # begin [-OPENFOR-] [-CLOSEDFOR-] openagain end
        return self.is_open_for_signup_rnd(time) or self.is_open_for_signup_fcfs(time)

    def until_signup_fmt(self):
        now = datetime.utcnow()
        delta = self.signup_begin - now

        # here we are in the closed window period; calculate delta to open again
        if delta.total_seconds() < 0:
            delta = (self.signup_begin + app.config['RANDOM_WINDOW_OPEN_FOR'] + app.config['RANDOM_WINDOW_CLOSED_FOR']) - now

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return '{0} Tage {1} Stunden {2} Minuten und einige Sekunden'.format(delta.days, hours, minutes)  # XXX: plural

    # In the following: sum(xs, []) basically is reduce(lambda acc x: acc + x, xs, [])
    def get_waiting_attendances(self):
        return sum(map(lambda course: course.get_waiting_attendances(), self.courses), [])

    def get_active_attendances(self):
        return sum(map(lambda course: course.get_active_attendances(), self.courses), [])

    def get_paying_attendances(self):
        return sum(map(lambda course: course.get_paying_attendances(), self.courses), [])

    def get_free_attendances(self):
        return sum(map(lambda course: course.get_free_attendances(), self.courses), [])


@total_ordering
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

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


@total_ordering
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

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


@total_ordering
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

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


@total_ordering
class Registration(db.Model):
    """Registration number for a :py:class:`Applicant` that is a student.

       :param number: The registration number

       Date is stored hashed+salted, so there is no way to get numbers from this
       model. You can only check if a certain, known number is stored in this
       table.
    """

    __tablename__ = 'registration'

    salted = db.Column(db.Binary(32), primary_key=True)

    def __init__(self, salted):
        self.salted = salted

    def __eq__(self, other):
        return self.number.lower() == other.number.lower()

    def __lt__(self, other):
        return self.number.lower() < other.number.lower()

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return '<Registration %r>' % hexlify(self.salted)

    @staticmethod
    def cleartext_to_salted(cleartext):
        """Convert cleartext unicode data to salted binary data."""
        return hash_secret(cleartext.lower())

    @staticmethod
    def from_cleartext(cleartext):
        """Return Registration instance from given cleartext string."""
        return Registration(Registration.cleartext_to_salted(cleartext))

    @staticmethod
    def exists(cleartext):
        """Checks if, for a given cleartext string, we store any valid registration."""
        registered = Registration.query.filter(
            Registration.salted == Registration.cleartext_to_salted(cleartext)
        ).first()
        return True if registered else False


# XXX: This should hold a ref to the specific language the rating is for
#      it's ok as of now, because we only got english test results.
@total_ordering
class Approval(db.Model):
    """Represents the approval for English courses a :py:class:`Applicant` aims for.

       :param tag: The registration number or other identification
       :param percent: applicant's level for English course
    """

    __tablename__ = 'approval'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), nullable=False)  # tag may be not unique, multiple tests taken
    percent = db.Column(db.Integer, nullable=False)

    percent_constraint = db.CheckConstraint(between(percent, 0, 100))

    def __init__(self, tag, percent):
        self.tag = tag
        self.percent = percent

    def __repr__(self):
        return '<Approval %r %r>' % (self.tag, self.percent)

    def __lt__(self, other):
        return self.percent < other.percent


class User(db.Model):
    """User for internal UI

       :param id: User ID, the email address most of the time.
       :param pwsalted: Salted password data.
    """

    __tablename__ = 'user'

    id = db.Column(db.String(120), primary_key=True)
    active = db.Column(db.Boolean, default=True)
    pwsalted = db.Column(db.Binary(32), nullable=True)

    def __init__(self, id):
        """Create new, active user without password."""
        self.id = id
        self.pwsalted = None

    def reset_password(self):
        """Reset password to random one and return it."""
        # choose random password
        rng = random.SystemRandom()
        pw = ''.join(
            rng.choice(string.ascii_letters + string.digits)
            for _ in range(0, 16)
        )
        self.pwsalted = hash_secret(pw)
        return pw

    def get_id(self):
        """Return user ID"""
        return self.id

    @property
    def is_active(self):
        """Report if user is active."""
        return self.active

    @property
    def is_anonymous(self):
        """Report if user is anonymous.

        This will return False everytime.
        """
        return False

    @property
    def is_authenticated(self):
        """Report if user is authenticated.

        This always returns True because we do not store that state.

        Also: we enable multiple systems to be locked in as the same user,
        because accounts might be shared amongst people.
        """
        return True

    def get_auth_token(self):
        """Get token that can be used to authentificate a user."""
        return token.generate(self.id, 'users')

    @staticmethod
    def get_by_token(tokenstring):
        """Return user by token string.

        Returns None if one of the following is true:
            - token is invalid
            - token is outdated
            - user does not exist.
        """
        id = token.validate_multi(tokenstring, 'users')
        if id:
            return User.query.filter(func.lower(User.id) == func.lower(id)).first()
        else:
            return None

    @staticmethod
    def get_by_login(id, pw):
        """Return user by ID and password.

        Returns None if one of the following is true:
            - ID does not exist
            - salted PW in database is set to None (i.e. no PW assigned)
            - password does not match (case-sensitive match!)
        """
        salted = hash_secret(pw)
        return User.query.filter(and_(
            func.lower(User.id) == func.lower(id),
            User.pwsalted != None,
            User.pwsalted == salted
        )).first()
