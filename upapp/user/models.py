from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from flask import jsonify

from upapp.db import Base, db_session

association_table = Table(
    'user_skill_associations', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('skill_id', Integer, ForeignKey('skills.id'), nullable=False),
    Column('level', Integer),
)


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
        user = db_session.query(User).filter(User.id == user_id).first().serialize()
        # TODO: - Raise if multiple
        return jsonify(user)

    @staticmethod
    def create(json):
        try:
            first_name = json['first_name']
            last_name = json['last_name']
            skills = [Skill.create(item) for item in json['skills']]
            user = User(first_name=first_name, last_name=last_name)
            for skill in skills:
                user.skills.append(skill)
            db_session.add(user)
            db_session.commit()
            user.cv_url = '/api/user/{user_id}'.format(user_id=user.id)
            # TODO - commit to times
            db_session.commit()
            return jsonify(user.serialize())
        except KeyError:
            # TODO: - Replace to own exception
            KeyError

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
    users = relationship(
        'User',
        secondary=association_table
    )

    @staticmethod
    def create(skill):
        try:
            name = skill['name']
            skill = db_session.query(Skill).filter(Skill.name == name).first() or Skill(name=name)
        except KeyError:
            pass
        db_session.add(skill)
        db_session.commit()
        return skill

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
