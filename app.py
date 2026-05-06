from flask import Flask, redirect, url_for
from config import config
from extensions import db, login_manager
from models.user import User
import os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import auth_bp
    from routes.todos import todos_bp
    from routes.categories import categories_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return redirect(url_for('todos.index'))

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)