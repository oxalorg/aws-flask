import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_CONFIG', 'development')])
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import oxblog.post