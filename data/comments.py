import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    expend_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("expend.id"))
    expend = sqlalchemy.orm.relationship('Expend', backref='expend')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = sqlalchemy.orm.relationship('Users', backref='users')

    expend = orm.relation('Expend')
    user = orm.relation('User')
