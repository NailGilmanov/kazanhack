from flask import Flask, render_template, redirect
from data import db_session
from waitress import serve
from flask_cors import CORS, cross_origin
import requests

from flask import jsonify

from forms.user import RegisterForm, LoginForm
from forms.expends import ExpendsForm
from forms.arrival import ArrivalsForm

from data.users import User
from data.expend import Expend

from flask_login import LoginManager, login_user

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register/<string:username>/<string:password>/<string:password_again>', methods=['GET', 'POST'])
def valid_register_data(username, password, password_again):
    form = RegisterForm()
    if form.validate_on_submit():
        if password != password_again:
            # Пароли не совпадают
            return jsonify("false")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == username).first():
            # Такой пользователь уже есть
            return jsonify("false")

    # Добавление в базу данных
    db_sess = db_session.create_session()
    user = User(
        name=username
    )
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()

    return jsonify(str(user.id))


@app.route('/login/<string:username>/<string:password>')
def valid_login_data(username, password):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.name == username).first()

    if user:
        if user.check_password(password):
            login_user(user)
            return jsonify(str(user.id))
        # Неправильный логин или пароль
    return jsonify('false')


@app.route("/new_expend/<int:id>/<string:date>/<int:category>/<int:price>/<int:user_id>",
           methods=['GET', 'POST'])
def new_expend(id, date, category, price, user_id):
    session = db_session.create_session()
    expend = Expend()
    expend.id = id
    expend.date = date
    expend.category = category
    expend.price = price
    expend.user_id = user_id
    session.add(expend)
    session.commit()
    return jsonify('true')
    # print(form.errors)


@app.route('/get_username/<int:id>')
def get_username(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    return user.name


@app.route("/get_expend/<int:id>",
           methods=['GET', 'POST'])
def get_expend(id):
    db_sess = db_session.create_session()
    expend = db_sess.query(Expend).filter(Expend.id == id).first()
    id = {"id": int(expend.id)}
    date = {"date":f"{expend.date}"}
    category = {"category": int(expend.category)}
    price = {"price": int(expend.price)}
    user_id = {"user_id": int(expend.user_id)}
    return id | date | category | price | user_id


def main():
    db_session.global_init('db/database.sqlite')
    serve(app, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
