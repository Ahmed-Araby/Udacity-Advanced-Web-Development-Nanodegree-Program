from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from flask_moment import Moment


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db);

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# relation ships

# many to many [venue - genre]
genre_venue = db.Table('genre_venue',
                       db.Column('genre_id', db.Integer,
                                 db.ForeignKey('genre.id',  ondelete='cascade', onupdate='cascade'), primary_key = True),
                       db.Column('venue_id', db.Integer,
                                 db.ForeignKey('venue.id',  ondelete='cascade', onupdate='cascade'), primary_key = True));

artist_genre = db.Table('artist_genre',
                        db.Column('genre_id', db.Integer,
                                  db.ForeignKey('genre.id',  ondelete='cascade', onupdate='cascade'), primary_key=True),
                        db.Column('artist_id', db.Integer,
                                  db.ForeignKey('artist.id',  ondelete='cascade', onupdate='cascade'), primary_key=True));


"""
this table cover the relation between artist and venue 
as one artists can work in multiple venus and 
one venue can have multiple artist 
and show is the name of the relationship between them.
"""

show = db.Table('show',
                db.Column('artist_id', db.Integer, db.ForeignKey('artist.id', ondelete='cascade', onupdate='cascade'), primary_key = True),
                db.Column('venue_id', db.Integer, db.ForeignKey('venue.id', ondelete='cascade', onupdate='cascade'), primary_key = True),
                db.Column('start_time', db.DateTime, primary_key = True),
                db.UniqueConstraint('artist_id', 'start_time', name='one_show_perVenue_atATime'),
                db.UniqueConstraint('venue_id', 'start_time', name='one_show_byArtist_atATime')
                );

class venue(db.Model):
    __tablename__ = 'venue';

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)   # withing a city
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # missing data
    website_link = db.Column(db.String(120));
    seeking_talent = db.Column(db.Boolean, default=False);
    seeking_description = db.Column(db.String);

    # relation ship  [ with genre ]
    genres = db.relationship('genre', secondary=genre_venue, backref='venues', lazy='joined', cascade='all, delete', passive_deletes=True);

    # relation ship [ with artist as show ]
    # lazy is True as I will use explicit join operation on show table
    # and artist to get artists that this venue is related to
    artists = db.relationship('artist', secondary='show', backref='venues', lazy=True, cascade='all, delete', passive_deletes=True);

    def __repr__(self):
        return "venue: id {} , name {} ".format(self.id, self.name);

class artist(db.Model):

    __tablename__ = 'artist';

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120),nullable = False)
    phone = db.Column(db.String(120),nullable = False)

    """
    removed data 
    this is replaced with a relation ship to another table, 
    in case we needed to do more features using this information 
    """
    # genres = db.Column(db.String(120))

    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # missing data
    website_link = db.Column(db.String(120));
    seeking_venue = db.Column(db.Boolean, default=False);
    seeking_description = db.Column(db.String);

    # relation ship
    genres = db.relationship('genre', secondary=artist_genre, backref='artists', lazy='joined', cascade='all, delete', passive_deletes=True);

    def __repr__(self):
      return "Artist: id {} , name {} ".format(self.id, self.name);


"""
[additional table]
I think that seprating genres as table give
more flexibility for adding more features , or more genres 
"""

class genre(db.Model):
    __tablename__ ='genre';
    id = db.Column(db.Integer, primary_key = True);
    name = db.Column(db.String, nullable = False, unique=True);

    def __repr__(self):
      return "id {},   name {}".format(self.id, self.name);

################ end of table models  ###################.