import os
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_required

from models.database import db
from models.wms.users import User 
from views import retail_app, wms_app, login_app


config_name = os.getenv('CONFIG_NAME', 'DevelopmentConfig')

app = Flask(__name__)
app.register_blueprint(wms_app)
app.register_blueprint(retail_app)
app.register_blueprint(login_app)

app.config.from_object(f'config.{config_name}')


db.init_app(app)
migrate = Migrate(app=app, db=db)
csrf=CSRFProtect(app)
login_manager = LoginManager(app=app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.get('/', endpoint='index')
@login_required
def index():
    return render_template('index.html')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_app.login') + '?next=' + request.url)
    
    return response


if __name__ == '__main__':
    app.run(
        debug=True,
    )
