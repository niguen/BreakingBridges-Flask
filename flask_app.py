from flask import Flask
from config import Config
from models_sqlite import db

def create_app(config_class=Config):
    app = Flask(__name__)

    #conf = Config()
    app.config.from_object(config_class)

    # initialize the app with the extension
    #db = SQLAlchemy(app)
    db.init_app(app)    

    # Initialize Flask extensions here

    # Register blueprints here
    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app

app = create_app()