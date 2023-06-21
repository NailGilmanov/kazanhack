import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String)
    # устанавливает значение хэша пароля для переданной строки, нужна для регистрации пользователя
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # проверяет, правильный ли пароль ввел пользователь, нужна для авторизации пользователей в
    # нашем приложении.
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
