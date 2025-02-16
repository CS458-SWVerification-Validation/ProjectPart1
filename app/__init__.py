from flask import Flask, redirect, url_for, render_template
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_cors import CORS

from config import config
from app.extensions import db
from app.models.user import User

def create_app(config_mode='development'):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins="*")
    app.config.from_object(config[config_mode])

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.getUserById(int(user_id))

    # Register blueprints here
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    @app.route('/')
    def splash():
        return redirect(url_for("auth.login"))
    
    @app.errorhandler(404)
    def page_not_found(e):
        print("bu ne awq")
        return render_template("404.html"), 200

    return app