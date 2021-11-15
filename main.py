from flask import Flask,request,abort,jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import db,Users

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config["JWT_SECRET_KEY"] = "kwehhehojowoojow"  #

jwt = JWTManager(app)

bcrypt = Bcrypt(app)

db.init_app(app)


with app.app_context():
    db.create_all()




@app.route("/register", methods= ["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    user_exist = Users.query.filter_by(email = email).first() is not None

    if user_exist:
        abort(409)

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = Users(name=name,email=email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.email)

    the_info = [new_user.adm, new_user.id,new_user.email]

    return jsonify({
        "token": access_token,
        "info":the_info,
        "Admstats":new_user.adm,
        "email": new_user.email,
        "status": 'success'
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = Users.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    #session["user_id"] = user.id

    access_token = create_access_token(identity=user.email)

    return jsonify({
        "id": user.id,
        "email": user.email,
        "adm": user.adm,
        "token": access_token
    })


if __name__ == '__main__':
    app.run(debug=True)

