import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

from sqlalchemy_serializer import SerializerMixin


class Expend(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'expend'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
