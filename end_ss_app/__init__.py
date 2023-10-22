from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
#load config
csrf = CSRFProtect(app)
db=SQLAlchemy(app) 




from end_ss_app import user_routes ,admin_routes