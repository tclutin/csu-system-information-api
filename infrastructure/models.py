from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class Roles(Base):
    __tablename__ = 'roles'

    role_name = Column(Text, primary_key=True)


class Specialty(Base):
    __tablename__ = "specialties"

    specialty_name = Column(Text, primary_key=True)


class Department(Base):
    __tablename__ = "departments"

    department_name = Column(Text, primary_key=True)


class FAQ(Base):
    __tablename__ = 'faq'

    faq_id = Column(BigInteger, primary_key=True)
    question = Column(Text, unique=True, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)


class Student(Base):
    __tablename__ = "students"

    student_id = Column(BigInteger, primary_key=True)
    fullname = Column(Text, nullable=False)
    group_id = Column(BigInteger, ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False)
    tgchat_id = Column(BigInteger, unique=True, nullable=False)
    student_card = Column(Text, nullable=False)

    group = relationship('Group', backref=backref('students', cascade='all, delete'))


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(BigInteger, primary_key=True)
    short_name = Column(Text, unique=True, nullable=False)
    department = Column(Text, ForeignKey('departments.department_name'), nullable=False)
    specialty = Column(Text, ForeignKey('specialties.specialty_name'), nullable=False)
    user_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)

    department_ref = relationship('Department', backref='groups')
    specialty_ref = relationship('Specialty', backref='groups')


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    role = Column(Text, ForeignKey('roles.role_name'), nullable=False)
    fullname = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)

    role_ref = relationship('Roles', backref='users')


class Status(Base):
    __tablename__ = 'status'

    status_name = Column(Text, primary_key=True)


class TicketType(Base):
    __tablename__ = 'types'

    type_ticket = Column(Text, primary_key=True)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(BigInteger, primary_key=True)
    status = Column(Text, ForeignKey('status.status_name'), nullable=False)
    type = Column(Text, ForeignKey('types.type_ticket'), nullable=False)
    tgchat_id = Column(BigInteger, nullable=False)
    fullname = Column(Text, nullable=True)
    wish_group = Column(Text, nullable=True)
    photo = Column(Text, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)

    status_ref = relationship('Status', backref='tickets')
    type_ref = relationship('TicketType', backref='tickets')
