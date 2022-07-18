from CONFIG import AppRun
from init import create_app
from flask_cors import CORS
from routes import user, recipe,search
import pymysql
from datetime import timedelta
from flask_jwt_extended import (create_access_token, current_user, jwt_required, JWTManager, create_refresh_token)


pymysql.install_as_MySQLdb()

app = create_app(__name__)
app.register_blueprint(user.bp, url_prefix="/user")
app.register_blueprint(recipe.bp, url_prefix="/recipe")
app.register_blueprint(search.bp, url_prefix="/search")
CORS(app)
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=10)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return dict(identity)

if __name__ == '__main__':
    app.run(host=AppRun.host, port=AppRun.port, debug=AppRun.debug)

