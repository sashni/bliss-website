import os
from flask import Flask, render_template, session
#from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
mail = None

def create_app():
    global mail
    app = Flask(__name__)
    app.testing = False
    app.config.from_object('config')

    @app.before_first_request
    def register_admin():
        from bliss.models import Admin
        admin = Admin.query.all()
        if admin == []:
            # Register Admin
            admin = Admin(email=app.config["ADMIN_USERNAME"], password=app.config["ADMIN_PASSWORD"])
            db.session.add(admin)
            db.session.commit()
            print('admin created', Admin.query.all())
        else:
            print('Admin exists', admin)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'store.page_not_found'
    #mail = Mail(app)

    with app.app_context():
        from . import store, admin

        app.register_blueprint(store.bp)
        app.register_blueprint(admin.bp)
        app.add_url_rule('/', endpoint='index')

        return app
