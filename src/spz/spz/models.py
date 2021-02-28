# -*- coding: utf-8 -*-

"""The application's models.

   Manages the mapping between abstract entities and concrete database models.
"""

from enum import Enum
from binascii import hexlify
from datetime import datetime, timedelta
from functools import total_ordering
import random
import string

from argon2 import argon2_hash

from sqlalchemy import and_, or_, between, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import select

from spz import app, db, token


def hash_secret_strong(s):
    """Hash secret, case-sensitive string to binary data.

    This is the strong version which should be used for passwords but not for
    huge data sets like indentification numbers.
    """
    if not s:
        s = ''

    # WARNING: changing these parameter invalides the entire table!
    # INFO: buflen is in bytes, not bits! So this is a 256bit output
    #       which is higher than the current (2015-12) recommendation
    #       of 128bit. We use 2 lanes and 4MB of memory. 4 passes seems
    #       to be a good choice.
    return argon2_hash(
        s.encode('utf8'),
        app.config['ARGON2_SALT'],
        buflen=32,
        t=4,
        p=2,
        m=(1 << 12)
    )


def hash_secret_weak(s):
    """Hash secret, case-sensitive string to binary data.

    This is the weak version which should be used for large data sets like
    identifiers, but NOT for passwords!
    """
    if not s:
        s = ''

    # WARNING: changing these parameter invalides the entire table!
    # INFO: buflen is in bytes, not bits! So this is a 256bit output
    #       which is higher than the current (2015-12) recommendation
    #       of 128bit. We use 2 lanes and 64KB of memory. One pass has
    #       to be enough, because otherwise we need to much time while
    #       importing.
    return argon2_hash(
        s.encode('utf8'),
        app.config['ARGON2_SALT'],
        buflen=32,
        t=1,
        p=2,
        m=(1 << 6)
    )


def verify_tag(tag):
    """Verifies, if a tag is already in the database.
    """
    return Registration.exists(tag)


@total_ordering
class Attendance(db.Model):
    """Associates an :py:class:`Applicant` to a :py:class:`Course`.

        Use the :py:func:`set_waiting_status` to remove the :py:data:`waiting` Status

       :param course: The :py:class:`Course` an :py:class:`Applicant` attends.
       :param graduation: The intended :py:class:`Graduation` of the :py:class:`Attendance`.
       :param waiting: Represents the waiting status of this :py:class`Attendance`.
       :param discount: Discount percentage for this :py:class:`Attendance` from 0 (no discount) to 100 (free).
       :param informed_about_rejection: Tells us if we already send a "you're (not) in the course" mail

       .. seealso:: the :py:data:`Applicant` member functions for an easy way of establishing associations
    """

    __tablename__ = 'attendance'

    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    course = db.relationship("Course", backref="attendances", lazy="joined")

    graduation_id = db.Column(db.Integer, db.ForeignKey('graduation.id'))
    graduation = db.relationship("Graduation", backref="attendances", lazy="joined")

    waiting = db.Column(db.Boolean)  # do not change, please use the set_waiting_status function
    discount = db.Column(db.Numeric(precision=3))
    amountpaid = db.Column(db.Numeric(precision=5, scale=2), nullable=False)

    paidbycash = db.Column(db.Boolean)  # could be remove, since cash payments are not allowed anyway

    registered = db.Column(db.DateTime(), default=datetime.utcnow)
    payingdate = db.Column(db.DateTime())
    signoff_window = db.Column(db.DateTime(), default=datetime.utcnow)

    informed_about_rejection = db.Column(db.Boolean, nullable=False, default=False)

    amountpaid_constraint = db.CheckConstraint(amountpaid >= 0)
    MAX_DISCOUNT = 100  # discount stored as percentage
    discount_constraint = db.CheckConstraint(between(discount, 0, MAX_DISCOUNT))

    def __init__(self, course, graduation, waiting, discount, informed_about_rejection=False):
        self.course = course
        self.graduation = graduation
        self.waiting = waiting
        self.discount = discount
        self.paidbycash = False
        self.amountpaid = 0
        self.payingdate = None
        self.informed_about_rejection = informed_about_rejection

    def __repr__(self):
        return '<Attendance %r %r>' % (self.applicant, self.course)

    def __lt__(self, other):
        return self.registered < other.registered

    def set_waiting_status(self, waiting_list):
        if self.waiting and not waiting_list:
            signoff_period = app.config['SELF_SIGNOFF_PERIOD']
            self.signoff_window = (datetime.utcnow() + signoff_period).replace(microsecond=0, second=0, minute=0)
            self.waiting = False
        elif not self.waiting and waiting_list:
            self.waiting = True

    @hybrid_property
    def is_free(self):
        return self.discount == self.MAX_DISCOUNT

    @hybrid_property
    def unpaid(self):
        return (1 - self.discount / self.MAX_DISCOUNT) * self.price - self.amountpaid

    @hybrid_property
    def is_unpaid(self):
        return self.unpaid > 0

    @hybrid_property
    def price(self):
        return self.course.price

    @price.expression
    def price(cls):
        return Course.price


@total_ordering
class Applicant(db.Model):
    """Represents a person, applying for one or more :py:class:`Course`.

       Use the :py:func:`add_course_attendance` and :py:func:`remove_course_attendance`
       member functions to associate a :py:class:`Applicant` to a specific :py:class:`Course`.

       :param mail: Mail address
       :param tag: System wide identification tag
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
    tag = db.Column(db.String(30), unique=False, nullable=True)  # XXX

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

    signoff_id = db.Column(db.String(120))

    registered = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, mail, tag, first_name, last_name, phone, degree, semester, origin):
        self.mail = mail
        self.tag = tag
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.degree = degree
        self.semester = semester
        self.origin = origin
        self.discounted = False
        rng = random.SystemRandom()
        self.signoff_id = ''.join(
            rng.choice(string.ascii_letters + string.digits)
            for _ in range(0, 16)
        )

    def __repr__(self):
        return '<Applicant %r %r>' % (self.mail, self.tag)

    def __lt__(self, other):
        return (self.last_name.lower(), self.first_name.lower()) < (other.last_name.lower(), other.first_name.lower())

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def add_course_attendance(self, *args, **kwargs):
        attendance = Attendance(*args, **kwargs)
        self.attendances.append(attendance)
        return attendance

    def remove_course_attendance(self, course):
        remove = [attendance for attendance in self.attendances if attendance.course == course]
        for attendance in remove:
            self.attendances.remove(attendance)
        return len(remove) > 0

    def is_student(self):
        return Registration.exists(self.tag)

    def best_rating(self):
        """Results best rating, prioritize sticky entries."""
        results_priority = [
            approval.percent
            for approval
            in Approval.get_for_tag(self.tag, True)
        ]
        if results_priority:
            return max(results_priority)

        results_normal = [
            approval.percent
            for approval
            in Approval.get_for_tag(self.tag, False)
        ]
        if results_normal:
            return max(results_normal)

        return 0

    """ Discount (factor) for the next course beeing entered """
    def current_discount(self):
        attends = len([attendance for attendance in self.attendances if not attendance.waiting])
        if self.is_student() and attends == 0:
            return Attendance.MAX_DISCOUNT  # one free course for students
        else:
            return Attendance.MAX_DISCOUNT / 2 if self.discounted else 0  # discounted applicants get 50% off

    def in_course(self, course):
        return course in [attendance.course for attendance in self.attendances]

    def active_in_parallel_course(self, course):
        # do not include the course queried for
        active_in_courses = [
            attendance.course
            for attendance
            in self.attendances
            if attendance.course != course and not attendance.waiting
        ]

        active_parallel = [
            crs
            for crs
            in active_in_courses
            if crs.language == course.language and (
                crs.level == course.level or
                crs.level in course.collision or
                course.level in crs.collision
            )
        ]

        return len(active_parallel) > 0

    # Management wants us to limit the global amount of attendances one is allowed to have.. so what can I do?
    def over_limit(self):
        now = datetime.utcnow()
        # at least do not count in courses that are already over..
        running = [att for att in self.attendances if att.course.language.signup_end >= now]
        return len(running) >= app.config['MAX_ATTENDANCES']

    def matches_signoff_id(self, signoff_id):
        return signoff_id == self.signoff_id

    def is_in_signoff_window(self, course):
        try:
            att = [attendance for attendance in self.attendances if course == attendance.course][0]
        except IndexError:
            return False
        return att.signoff_window > datetime.utcnow()

    @property
    def doppelgangers(self):
        if not self.tag or self.tag == 'Wird nachgereicht':
            return []
        return Applicant.query \
            .filter(Applicant.tag == self.tag) \
            .filter(Applicant.mail != self.mail) \
            .all()

    def has_submitted_tag(self):
        return self.tag and self.tag != 'Wird nachgereicht'


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
       :param collision: Levels that collide with this course.
       :param has_waiting_list: Indicates if there is a waiting list for this course

       .. seealso:: the :py:data:`attendances` relationship
    """

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    level = db.Column(db.String(120), nullable=False)
    alternative = db.Column(db.String(10), nullable=True)
    limit = db.Column(db.Integer, nullable=False)  # limit is SQL keyword
    price = db.Column(db.Integer, nullable=False)
    ger = db.Column(db.String(10), nullable=True)
    rating_highest = db.Column(db.Integer, nullable=False)
    rating_lowest = db.Column(db.Integer, nullable=False)
    collision = db.Column(postgresql.ARRAY(db.String(120)), nullable=False)
    has_waiting_list = db.Column(db.Boolean, nullable=False, default=False)

    unique_constraint = db.UniqueConstraint(language_id, level, alternative, ger)
    limit_constraint = db.CheckConstraint(limit > 0)
    price_constraint = db.CheckConstraint(price > 0)
    rating_constraint = db.CheckConstraint(and_(
        between(rating_highest, 0, 100),
        between(rating_lowest, 0, 100),
        rating_lowest <= rating_highest
    ))

    def __init__(
        self, language, level, alternative, limit, price, ger=None, rating_highest=100, rating_lowest=0, collision=[]
    ):
        self.language = language
        self.level = level
        self.alternative = alternative
        self.limit = limit
        self.price = price
        self.ger = ger
        self.rating_highest = rating_highest
        self.rating_lowest = rating_lowest
        self.collision = collision

    def __repr__(self):
        return '<Course %r>' % (self.full_name)

    def __lt__(self, other):
        return (self.language, self.level.lower()) < (other.language, other.level.lower())

    def allows(self, applicant):
        return self.rating_lowest <= applicant.best_rating() <= self.rating_highest

    def has_rating_restrictions(self):
        return self.rating_lowest > 0 or self.rating_highest < 100

    """ Retrieves all attendances, that match a certain criteria.
        Criterias can be set to either True, False or to None (which includes both).
       :param waiting: Whether the attendant is on the waiting list
       :param is_unpaid: Whether the course fee is still (partially) unpaid
       :param is_free: Whether the course is fully discounted
    """
    def filter_attendances(self, waiting=None, is_unpaid=None, is_free=None):
        result = []
        for att in self.attendances:
            valid = True
            if waiting is not None:
                valid &= att.waiting == waiting
            if is_unpaid is not None:
                valid &= att.is_unpaid == is_unpaid
            if is_free is not None:
                valid &= att.is_free == is_free
            if valid:
                result.append(att)
        return result

    def has_attendance_for_tag(self, tag):
        return len(self.get_attendances_for_tag(tag)) > 0

    def get_waiting_attendances(self):
        return [attendance for attendance in self.attendances if attendance.waiting]

    def get_active_attendances(self):
        return [attendance for attendance in self.attendances if not attendance.waiting]

    @hybrid_method
    def count_attendances(self, *args, **kw):
        return len(self.filter_attendances(*args, **kw))

    @count_attendances.expression
    def count_attendances(cls, waiting=None, is_unpaid=None, is_free=None):
        query = select([func.count(Attendance.applicant_id)]).where(Attendance.course_id == cls.id)
        if waiting is not None:
            query = query.where(Attendance.waiting == waiting)
        if is_unpaid is not None:
            query = query.where(Attendance.is_unpaid == is_unpaid)
        if is_free is not None:
            query = query.where(Attendance.is_free == is_free)
        return query.label("attendance_count")

    @hybrid_property
    def vacancies(self):
        return self.limit - self.count_attendances(waiting=False)

    @hybrid_property
    def is_full(self):
        return self.vacancies <= 0

    @hybrid_property
    def is_overbooked(self):
        return self.count_attendances() >= (self.limit * app.config['OVERBOOKING_FACTOR'])

    def get_attendances_for_tag(self, tag):
        return [attendance for attendance in self.attendances if attendance.applicant.tag == tag]

    @property
    def full_name(self):
        result = '{0} {1}'.format(self.language.name, self.level)
        if self.alternative:
            result = '{0} {1}'.format(result, self.alternative)
        return result

    """ active attendants without debt """
    @property
    def course_list(self):
        list = [attendance.applicant for attendance in self.filter_attendances(waiting=False)]
        list.sort()
        return list

    class Status(Enum):
        VACANCIES = 1
        LITTLE_VACANCIES = 2
        SHORT_WAITINGLIST = 4
        FULL = 8

    @property
    def status(self):
        if self.is_full:
            if self.count_attendances(waiting=True) <= app.config['SHORT_WAITING_LIST']:
                return self.Status.SHORT_WAITINGLIST
            else:
                return self.Status.FULL
        else:
            if self.vacancies <= app.config['LITTLE_VACANCIES']:
                return self.Status.LITTLE_VACANCIES
            else:
                return self.Status.VACANCIES


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
    signup_rnd_window_end = db.Column(db.DateTime())
    signup_manual_end = db.Column(db.DateTime())
    signup_end = db.Column(db.DateTime())
    signup_auto_end = db.Column(db.DateTime())

    signup_constraint = db.CheckConstraint(signup_end > signup_begin)

    def __init__(self, name, reply_to, signup_begin, signup_rnd_window_end, signup_manual_end, signup_end,
                 signup_auto_end):
        self.name = name
        self.reply_to = reply_to
        self.signup_begin = signup_begin
        self.signup_rnd_window_end = signup_rnd_window_end
        self.signup_manual_end = signup_manual_end
        self.signup_end = signup_end
        self.signup_auto_end = signup_auto_end

    def __repr__(self):
        return '<Language %r>' % self.name

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    @property
    def signup_rnd_begin(self):
        return self.signup_begin

    @property
    def signup_rnd_end(self):
        return self.signup_rnd_window_end

    @property
    def signup_manual_begin(self):
        # XXX: find something better
        return datetime.min

    @property
    def self_signoff_end(self):
        return self.signup_manual_end + app.config['SELF_SIGNOFF_PERIOD']

    @property
    def signup_fcfs_begin(self):
        return self.signup_rnd_end + app.config['RANDOM_WINDOW_CLOSED_FOR']

    @property
    def signup_fcfs_end(self):
        return self.signup_end

    def is_open_for_self_signoff(self, time):
        return time < self.self_signoff_end

    def is_open_for_signup_rnd(self, time):
        return self.signup_rnd_begin < time < self.signup_rnd_end < self.signup_end

    def is_open_for_signup_fcfs(self, time):
        return self.signup_fcfs_begin < time < self.signup_fcfs_end

    def is_open_for_signup(self, time):
        # management wants the system to be: open a few hours,
        # then closed "overnight" for random selection, then open again.
        # begin [-OPENFOR-] [-CLOSEDFOR-] openagain end
        return self.is_open_for_signup_rnd(time) or self.is_open_for_signup_fcfs(time)

    def is_upcoming(self, time):
        return self.signup_end >= time and self.signup_begin - time < timedelta(days=2)

    def is_in_manual_mode(self, time):
        return (time < self.signup_manual_end) or (time > self.signup_auto_end)

    def until_signup_fmt(self):
        now = datetime.utcnow()
        delta = self.signup_begin - now

        # here we are in the closed window period; calculate delta to open again
        if delta.total_seconds() < 0:
            delta = self.signup_fcfs_begin - now

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return '{0} Tage {1} Stunden {2} Minuten und einige Sekunden'.format(delta.days, hours, minutes)  # XXX: plural

    def count_attendances(self, *args, **kw):
        count = 0
        for course in self.courses:
            count += course.count_attendances(*args, **kw)
        return count


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
       :param validate_registration: do people of this origin have to provide a valid registration number?
    """

    __tablename__ = 'origin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    short_name = db.Column(db.String(10), nullable=False)
    validate_registration = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, short_name, validate_registration):
        self.name = name
        self.short_name = short_name
        self.validate_registration = validate_registration

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

    salted = db.Column(db.LargeBinary(32), primary_key=True)

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
        if cleartext:
            return hash_secret_weak(cleartext.lower())
        else:
            return hash_secret_weak('')

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

       :param tag_salted: The registration number or other identification, salted and hashed
       :param percent: applicant's level for English course
       :param sticky: describes that the entry is created for a special reason
       :param priority: describes that the entry has a higher priority than normal ones

       sticky entries:
        - are considered manual data; they are there for a special reason
        - should never be removed by a bot / syncing service

       non-sticky entries:
        - are considered automated data
        - should never be removed, added or modified by humans
        - can appear, disappear or change any time (e.g. because of syncing)
    """

    __tablename__ = 'approval'

    id = db.Column(db.Integer, primary_key=True)
    tag_salted = db.Column(db.LargeBinary(32), nullable=False)  # tag may be not unique, multiple tests taken
    percent = db.Column(db.Integer, nullable=False)
    sticky = db.Column(db.Boolean, nullable=False, default=False)
    priority = db.Column(db.Boolean, nullable=False, default=False)

    percent_constraint = db.CheckConstraint(between(percent, 0, 100))

    def __init__(self, tag, percent, sticky, priority):
        self.tag_salted = Approval.cleartext_to_salted(tag)
        self.percent = percent
        self.sticky = sticky
        self.priority = priority

    def __repr__(self):
        return '<Approval %r %r>' % (self.tag_salted, self.percent)

    def __lt__(self, other):
        return self.percent < other.percent

    @staticmethod
    def cleartext_to_salted(cleartext):
        """Convert cleartext unicode data to salted binary data."""
        if cleartext:
            return hash_secret_weak(cleartext.lower())
        else:
            return hash_secret_weak('')

    @staticmethod
    def get_for_tag(tag, priority=None):
        """Get all approvals for a specific tag and priority.

           :param tag: tag (as cleartext) you're looking for
           :param priority: optional priority to filter for
        """
        if priority is not None:
            return Approval.query.filter(and_(
                Approval.tag_salted == Approval.cleartext_to_salted(tag),
                Approval.priority == priority
            )).all()
        else:
            return Approval.query.filter(
                Approval.tag_salted == Approval.cleartext_to_salted(tag)
            ).all()


# helper table for User<--[admin]-->Language N:M relationship
admin_table = db.Table(
    'admin',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id')),
)


class User(db.Model):
    """User for internal UI

       :param id: User ID, for internal usage.
       :param email: Qualified user mail address.
       :param active: Describes if user is able to login.
       :param superuser: Users with that property have unlimited access.
       :param pwsalted: Salted password data.
       :param languages: For non-superusers that are the languages they have access to.
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean, default=True)
    superuser = db.Column(db.Boolean, default=False)
    pwsalted = db.Column(db.LargeBinary(32), nullable=True)
    languages = db.relationship('Language', secondary='admin', backref='admins')

    def __init__(self, email, active, superuser, languages):
        """Create new user without password."""
        self.email = email
        self.active = active
        self.superuser = superuser
        self.pwsalted = None
        self.languages = languages

    def reset_password(self):
        """Reset password to random one and return it."""
        # choose random password
        rng = random.SystemRandom()
        pw = ''.join(
            rng.choice(string.ascii_letters + string.digits)
            for _ in range(0, 16)
        )
        self.pwsalted = hash_secret_strong(pw)
        return pw

    def get_id(self):
        """Return user ID"""
        return self.id

    def can_edit_course(self, course):
        """Check if user can edit/admin a specific course."""
        return self.superuser or (course.language in self.languages)

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
        """Get token that can be used to authenticate a user."""
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
            return User.query.filter(User.id == int(id)).first()
        else:
            return None

    @staticmethod
    def get_by_login(email, pw):
        """Return user by email and password.

        Returns None if one of the following is true:
            - email does not exist
            - salted PW in database is set to None (i.e. no PW assigned)
            - password does not match (case-sensitive match!)
        """
        salted = hash_secret_strong(pw)
        return User.query.filter(and_(
            func.lower(User.email) == func.lower(email),
            User.pwsalted != None,  # NOQA
            User.pwsalted == salted
        )).first()


@total_ordering
class LogEntry(db.Model):
    """Log entry representing some DB changes

       :param id: unique ID
       :param timestamp: timestamp of the underlying event
       :param msg: log message (in German) describing the event
       :param language: course language the event belongs to, might be NULL (= global event)
    """
    __tablename__ = 'logentry'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    msg = db.Column(db.String(140), nullable=False)
    language = db.relationship("Language")  # no backref
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

    def __init__(self, timestamp, msg, language=None):
        self.timestamp = timestamp
        self.msg = msg
        self.language = language

    def __repr__(self):
        msg = self.msg
        if len(msg) > 10:
            msg = msg[:10] + '...'
        return '<LogEntry {} "{}" {}>'.format(self.timestamp, msg, self.language)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    @staticmethod
    def get_visible_log(user, limit=None):
        """Returns all log entries relevant for the given user."""
        entries = LogEntry.query.order_by(LogEntry.timestamp.desc()).all()

        if not user.superuser and limit is not None:
            entries = [x for x in entries if x.language is None or x.language in user.languages][:limit]
        elif not user.superuser:
            entries = [x for x in entries if x.language is None or x.language in user.languages]
        elif limit is not None:
            entries = entries[:limit]

        return entries


@total_ordering
class ExportFormat(db.Model):
    """Format used when exporting course lists

       :param id: unique ID
       :param name: human readable name for the format
       :param formatter: class name of the python formatter to be used
       :param template: optional template descriptor, supplied to the formatter
       :param language: language for which the export format is intended (NULL for any)
    """
    __tablename__ = 'export_format'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    formatter = db.Column(db.String(50), nullable=False)
    template = db.Column(db.String(50))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    language = db.relationship("Language")

    def __init__(self, name, formatter, template=None, extension=None, language=None):
        self.name = name
        self.formatter = formatter
        self.template = template
        self.language = language

    def __repr__(self):
        return '<ExportFormat "{}">'.format(self.descriptive_name)

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    @property
    def descriptive_name(self):
        return self.name

    @staticmethod
    def list_formatters(languages=[]):
        language_ids = [lang.id for lang in languages]
        return ExportFormat.query.filter(or_(
            ExportFormat.language == None,  # NOQA
            ExportFormat.language_id.in_(language_ids)
        )).all()
