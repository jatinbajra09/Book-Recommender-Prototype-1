from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Replace 'sqlite:///site.db' with your actual database URI if needed
engine = create_engine('sqlite:///site.db')
db.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
