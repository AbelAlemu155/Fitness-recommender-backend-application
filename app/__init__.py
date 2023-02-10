from flask import Flask, render_template, g
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login  import LoginManager
from flask_pagedown import PageDown
from flask_migrate import Migrate
from flask_msearch import Search


search = Search()


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view='auth.login'
pagedown = PageDown()
migrate=Migrate()




def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    search.init_app(app)

    # attach routes and custom error pages here
    return app
