from flask import Flask
from flask_restx import Api
from .models.views import Course, Student, User, StudentCourse, Admin
from .utils import db
from .config.config import config_dict
from flask_migrate import Migrate
from .enrollment.students import student_namespace
from .admin.views import admin_namespace
from .enrollment.courses import course_namespace
from .auth.views import auth_namespace 
from flask_jwt_extended import JWTManager, jwt_manager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

def create_app(config=config_dict['dev']):
    app = Flask(__name__)


    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    migrate = Migrate(app,db)

    api = Api(app)

    api.add_namespace(student_namespace)
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(admin_namespace, path='/admin')


    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Course': Course,
            'Student': Student

        }
    
    return app