from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# setup

db = SQLAlchemy();

def setUpDataBase(app, dataBase_url=None):
    if dataBase_url !=None:
        app.config['SQLALCHEMY_DATABASE_URI'] = dataBase_url;

    # what is the use of theses !!??
    db.app = app;
    db.init_app(app);
    migrate = Migrate(app, db);
    # db.create_all() # no need for it as we are using migrations.
    return;



# models
class books(db.Model):
    __tablename__ = 'books';
    id = db.Column(db.Integer, primary_key = True);
    name = db.Column(db.String(100), nullable=False);
    category = db.Column(db.String(100));
    rank = db.Column(db.Integer, default=1);

    def __repr__(self):
        return "ID: {}, Name: {}, Category: {}"\
            .format(self.id, self.name, self.category);

    def format(self):
        return {
            "id":self.id,
            "name":self.name,
            "category":self.category
        }