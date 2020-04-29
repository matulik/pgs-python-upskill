from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from flask import jsonify

from upapp.aws.aws import AWS
from upapp.db import Base, db_session

association_table = Table(
    'user_skill_associations', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('skill_id', Integer, ForeignKey('skills.id'), nullable=False),
    Column('level', Integer),
)


class UserDoesNotExists(BaseException):
    pass


class UserCreationFailed(BaseException):
    pass


class FileUploadFiled(BaseException):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String())
    last_name = Column(String())
    cv_url = Column(String())
    skills = relationship(
        'Skill',
        secondary=association_table
    )

    @staticmethod
    def all():
        items = [item.serialize() for item in db_session.query(User).all()]
        return jsonify(items)

    @staticmethod
    def user(user_id):
        user = db_session.query(User).get(user_id)
        if user is not None:
            return jsonify(user.serialize())
        else:
            raise UserDoesNotExists()

    @staticmethod
    def delete(user_id):
        user = db_session.query(User).get(user_id)
        if user is not None:
            db_session.delete(user)
            db_session.commit()
        else:
            raise UserDoesNotExists()

    @staticmethod
    def create(json):
        user = None

        try:
            first_name = json['first_name']
            last_name = json['last_name']
            skills = [Skill.create(item) for item in json['skills']]
            user = User(first_name=first_name, last_name=last_name)
            [user.skills.append(skill) for skill in skills]
            db_session.add(user)
            db_session.commit()
            return jsonify(user.serialize())
        except KeyError:
            raise UserCreationFailed()

    @staticmethod
    def upload(user_id, file):
        if file is not None:
            user = db_session.query(User).get(user_id)
            aws = AWS()
            object_name = 'upskill/{user_id}/cv.pdf'.format(user_id=user_id)
            aws.upload(
                key=object_name,
                data=file
            )

            user.cv_url = aws.create_presigned_url(object_name) or ''
            return user.serialize()

        else:
            raise FileUploadFiled()

    def __init__(self, first_name=None, last_name=None, cv_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.cv_url = cv_url

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cv_url': self.cv_url,
            'skills': self.serialize_skills()
        }

    def serialize_skills(self):
        return [item.serialize() for item in self.skills]


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False, unique=True)
    level = Column(Integer)
    users = relationship(
        'User',
        secondary=association_table
    )

    @staticmethod
    def create(skill):
        try:
            name = skill['name']
            level = skill['level']
            skill = db_session.query(Skill).filter(Skill.name == name).first() or Skill(name=name, level=level)
        except KeyError:
            pass
        db_session.add(skill)
        db_session.commit()
        return skill

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level
        }
