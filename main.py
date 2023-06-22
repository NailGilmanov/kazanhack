import datetime
from flask import Flask
from data import db_session
from waitress import serve
from flask_cors import CORS
from flask import jsonify

from forms.user import RegisterForm

from data.users import User
from data.expend import Expend
from data.arrival import Arrival

from flask_login import LoginManager, login_user

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret_key'
app.config['JSON_AS_ASCII'] = False

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


@app.route('/register/<string:username>/<string:password>/<string:password_again>/<string:about>', methods=['GET', 'POST'])
def valid_register_data(username, password, password_again, about):
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
    user = User()
    user.name = username
    user.about = about
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


@app.route("/new_expend/<string:title>/<string:category>/<int:price>/<int:user_id>",
           methods=['GET', 'POST'])
def new_expend(title, category, price, user_id):
    session = db_session.create_session()
    expend = Expend()
    expend.title = title.capitalize()
    expend.date = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))
    expend.category = category.capitalize()
    expend.price = price
    expend.user_id = user_id
    session.add(expend)
    session.commit()
    return jsonify('true')


@app.route('/get_username/<int:id>')
def get_username(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    return user.name


@app.route('/get_user/<int:id>')
def get_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    dic = {}
    dic["id"] = user.id
    dic["name"] = user.name
    dic["about"] = user.about
    return dic


@app.route("/get_expend/<int:user_id>")
def get_expend(user_id):
    db_sess = db_session.create_session()
    expends = db_sess.query(Expend).filter(Expend.user_id == user_id).all()
    result = []
    for expend in expends:
        dic = {}
        dic["id"] = expend.id
        dic["title"] = expend.title
        dic["date"] = expend.date
        dic["category"] = expend.category
        dic["price"] = expend.price
        dic["user_id"] = expend.user_id
        result.append(dic)
    return jsonify(result)


@app.route("/get_expend_some/<int:user_id>")
def get_expend_some(user_id):
    db_sess = db_session.create_session()
    expends = db_sess.query(Expend).filter(Expend.user_id == user_id).all()
    result = 0
    for expend in expends:
        price = int(expend.price)
        result += price
    return jsonify(result)


@app.route("/new_arrival/<string:title>/<int:price>/<int:user_id>",
           methods=['GET', 'POST'])
def new_arrival(title, price, user_id):
    session = db_session.create_session()
    arrival = Arrival()
    arrival.title = title.capitalize()
    arrival.date = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))
    arrival.price = price
    arrival.user_id = user_id
    session.add(arrival)
    session.commit()
    return jsonify('true')


@app.route("/get_arrival/<int:user_id>")
def get_arrival(user_id):
    db_sess = db_session.create_session()
    arrivals = db_sess.query(Arrival).filter(Arrival.user_id == user_id).all()
    result = []
    for arrival in arrivals:
        dic = {}
        dic["id"] = arrival.id
        dic["title"] = arrival.title
        dic["date"] = arrival.date
        dic["price"] = arrival.price
        dic["user_id"] = arrival.user_id
        result.append(dic)
    return jsonify(result)


@app.route("/get_history/<int:user_id>")
def get_history(user_id):
    db_sess = db_session.create_session()
    arrivals = db_sess.query(Arrival).filter(Arrival.user_id == user_id).all()
    expends = db_sess.query(Expend).filter(Expend.user_id == user_id).all()
    result = []
    for arrival in arrivals:
        dic = {}
        dic["id"] = str(arrival.id)
        dic["title"] = arrival.title
        dic["date"] = arrival.date
        dic["category"] = "Пополнение"
        dic["price"] = f'+{arrival.price}'
        dic["user_id"] = str(arrival.user_id)
        result.append(dic)
    for expend in expends:
        dic = {}
        dic["id"] = str(expend.id)
        dic["title"] = expend.title
        dic["date"] = expend.date
        dic["category"] = str(expend.category)
        dic["price"] = f"-{expend.price}"
        dic["user_id"] = str(expend.user_id)
        result.append(dic)
    result = sorted(result, key=lambda x: x["date"], reverse=True)
    return result


@app.route("/get_analitics/<int:user_id>")
def get_analitics(user_id):
    db_sess = db_session.create_session()
    expends = db_sess.query(Expend).filter(Expend.user_id == user_id).all()
    res = {}
    procent = {}
    counter = 0
    for expend in expends:
        category = expend.category
        price = expend.price
        counter += price
        if category not in res:
            res[category] = price
        elif category in res:
            res[category] += price
    for category in res:
        proc = res[category] * 100 / counter
        procent[category] = round(proc, 2)
    return procent


def main():
    db_session.global_init('db/database.sqlite')
    serve(app, host='127.0.0.1', port=5000)


if __name__ == '__main__':
    main()
