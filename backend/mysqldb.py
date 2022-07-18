from init import db
from dataclasses import dataclass
import flask
from CONFIG import DatabaseConfig
from werkzeug.security import generate_password_hash, check_password_hash



@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(32), unique=True)
    role = db.Column(db.Enum("contributor", "explorer"))
    follow = db.Column(db.String(256))



'''
@dataclass
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(256))
'''


@dataclass
class Recipe(db.Model):
    __tablename__ = 'recipes'
    Rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipeName = db.Column(db.String(256))
    description = db.Column(db.Text)
    uploader = db.Column(db.Integer)
    ingredients = db.Column(db.Text)
    ingredientWeight = db.Column(db.Text)
    steps = db.Column(db.Text)
    type = db.Column(db.Text)
    comment = db.Column(db.String(256))
    grade = db.Column(db.Float)


def insert_db():
    users = []
    user = User()
    user.name = "admin1"
    user.password = generate_password_hash("admin1")
    user.email = "admin1@hotmail.com"
    users.append(user)
    db.session.add_all(users)
    db.session.commit()
    #roles = []
    #role = Role()
    # role.name="contributor"
    # role.description = "recipe contributor"
    # roles.append(role)
    # role = Role()
    # role.name = "explorer"
    # role.description = "recipe explorer"
    # roles.append(role)
    # db.session.add_all(roles)
    # db.session.commit()


if __name__ == '__main__':
    app = flask.Flask(__name__)
    app.config.from_object(DatabaseConfig)
    db.init_app(app)
    with app.app_context():
        insert_db()





