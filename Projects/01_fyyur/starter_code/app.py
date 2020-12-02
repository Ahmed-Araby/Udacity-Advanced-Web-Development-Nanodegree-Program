"""
******************* You need to run file "buildGenreTable.py"  once as this file will insert the data into genre table ***************************
before there was no data in the genre table which raised error on inserting  a venue.
"""
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import func
from datetime import  datetime
from models import *




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"

  elif format =='postgres_timeStamp':
      format ='EEEE MM'
  return babel.dates.format_datetime(date, format, locale='en')

# another function for formating date
def postgres_timeStamp_format(dateTimeObj):
    format = "%Y-%m-%d %H:%M:%S"; # postgres time stamp format.
    return dateTimeObj.strftime(format);

app.jinja_env.filters['datetime'] = format_datetime   # ** for jinja **

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # upcomming events only into count
  result1_all = db.session.query(venue.id, venue.name, venue.state, venue.city, func.count(show.c.start_time))\
                                .outerjoin(show)\
                                .group_by(venue.id, venue.name, venue.state, venue.city)\
                                .order_by(venue.state, venue.city)\
                                .all();

  result2_past = db.session.query(venue.id, func.count(show.c.start_time)) \
      .outerjoin(show) \
      .filter(show.c.start_time < postgres_timeStamp_format(datetime.now())) \
      .group_by(venue.id, venue.name, venue.state, venue.city) \
      .order_by(venue.state, venue.city) \
      .all();

  print(result1_all);
  print(result2_past);

  subtract = {};
  for record in result2_past:
      subtract[record[0]] = record[1];

  # build the data strcuture
  # group them by city and state
  # order by in the query allow us to do so as similer cityies and states will be adjacent rows.

  prevCity = "";
  prevState = "";
  data = [];
  venuesGroup = {};

  index = 0;
  while index < len(result1_all):

    # record is (0-id , 1-name, 2-state, 3-city, 4-count).
    record = result1_all[index];

    if (prevCity == "" and prevState == ""): # first time in each group.
        venuesGroup['city']  = record[3];
        venuesGroup['state'] = record[2];
        sub = subtract.get(record[0], 0);

        currentVenue = {"id":record[0], "name":record[1], "num_upcoming_shows":record[4] - sub};
        venuesGroup['venues'] = [currentVenue];

        prevCity = record[3];
        prevState = record[2];
        index +=1;

    elif prevState == record[2] and prevCity == record[3]:  # same group
        sub = subtract.get(record[0], 0);
        currentVenue = {"id": record[0], "name": record[1], "num_upcoming_shows": record[4] - sub};
        venuesGroup['venues'].append(currentVenue);
        index +=1;
    else:
      data.append(venuesGroup);
      venuesGroup = {}; # to avoid writing over the same reference.
      prevState = "";
      prevCity = "";

  if len(result1_all) > 0:
      """
      last group or the only exist group.
      """
      data.append(venuesGroup);
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term'];
  result = db.session.query(venue.id, venue.name, func.count(show.c.start_time))\
                            .outerjoin(show) \
                            .filter(func.lower(venue.name).like("%" + func.lower(search_term) + "%")) \
                            .filter((show.c.start_time >= postgres_timeStamp_format(datetime.now())) | (show.c.start_time == None)) \
                            .group_by(venue.id, venue.name)\
                            .all();

  response = {'count':len(result), "data":[]};
  for record in result:
      tmpObj = {"id":record[0], "name":record[1], "num_upcoming_shows":record[2]};
      response['data'].append(tmpObj);

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  """
    3 queries to the data base
      - get the artist
      - get past shows
      - get upcomming shows
      -** get genres -- but this one was loaded with the artist query.

      another way to do this is to join the 3 tables toogeateher  at once and this will be the only
      query to the data base then classify hte events here in the server (past and upcomming)
      but this will cuz in duplicate for the venue information returned from the data base
      + join operation is more expensive then select !!!
      which is better !!!!!.
  """

  # get the artist
  venueObj = db.session.query(venue).get(venue_id);
  venueId = venueObj.id;

  past_showsOfCurVenue= db.session.query(show.c.start_time, artist.id, artist.name, artist.image_link)\
                                            .join(artist)\
                                            .filter(show.c.start_time < postgres_timeStamp_format(datetime.now()))\
                                            .filter(show.c.venue_id == venueId)\
                                           .all();

  upcomming_showsOfCurVenue = db.session.query(show.c.start_time, artist.id, artist.name, artist.image_link) \
                                          .join(artist) \
                                          .filter(show.c.start_time >= postgres_timeStamp_format(datetime.now())) \
                                          .filter(show.c.venue_id == venueId) \
                                          .all();
  genresList = venueObj.genres;
  genres = [];
  for genreObj in genresList:
      genres.append(genreObj.name);

  data={
    "id": venueObj.id,
    "name": venueObj.name,
    "genres": genres,
    "address": venueObj.address,
    "city": venueObj.city,
    "state": venueObj.state,
    "phone": venueObj.phone,
    "website": venueObj.website_link,
    "facebook_link": venueObj.facebook_link,
    "seeking_talent": venueObj.seeking_talent,
    "seeking_description":venueObj.seeking_description,
    "image_link": venueObj.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": len(past_showsOfCurVenue),
    "upcoming_shows_count": len(upcomming_showsOfCurVenue),
  }

  # assign past shows.
  for record in past_showsOfCurVenue:
      tmpObj = {"start_time":postgres_timeStamp_format(record[0]),
                "venue_id":record[1], "venue_name":record[2],
                  "image_link":record[3]};
      data['past_shows'].append(tmpObj);

  # assign upcomming shows.
  for record in upcomming_showsOfCurVenue:
      tmpObj = {"start_time":postgres_timeStamp_format(record[0]),
                "venue_id":record[1], "venue_name":record[2],
                  "image_link":record[3]};
      data['upcoming_shows'].append(tmpObj);

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  submit_form = VenueForm(); # this is supposed to hold the data
  if not submit_form.validate_on_submit():
        print("error happens in validation");
        return render_template('forms/new_venue.html', form=submit_form);

  form = request.form.to_dict();

  form.pop('genres');
  genres = request.form.getlist('genres');
  seeking = False;
  seeking_description = "";

  if "seeking" in form:
      seeking = True;
      seeking_description = form['seeking_description'];

  try:
    newVenue = venue(name=form['name'], city=form['city'], state=form['state'],
                       phone=form['phone'], image_link=form['image_link'],
                       facebook_link=form['facebook_link'], website_link=form['website_link'],
                       seeking_talent=seeking, address=form['address']);
    if seeking:
      newVenue.seeking_description = seeking_description;

    db.session.add(newVenue);
    db.session.flush();
    venueId = newVenue.id;
    # insert the genres
    for genId in genres:
        sqlQuery = genre_venue.insert().values(genre_id = genId, venue_id = venueId);
        db.session.execute(sqlQuery);
    db.session.commit();
    flash('Venue ' +  form['name'] + ' was successfully listed!');
    print("inserted successfully");
  except Exception as err:
    print("error happens", err);
    db.session.rollback();
    flash('An error occurred. Venue ' + form['name'] + ' could not be listed.')

  finally:
    db.session.close();
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE', 'POST'])
def delete_venue(venue_id):
  error_happens = False;

  try:
    db.session.query(venue).filter_by(id=venue_id).delete(); # bulk delete
    db.session.commit();
    print("deleted successfuly");
  except:
    print("failed in deleting");
    error_happens = True;
    db.session.rollback(); # this remove the effect of this query from our APP context.
  finally:
    db.session.close();

  """
  BOnuS is implemented -- a button that triger post request 
  """

  # redirect take the name of the function
  if not error_happens:
    return redirect(url_for('index'));
  else:
    return redirect(url_for('show_venue', venue_id = venue_id));

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  results = db.session.query(artist.id, artist.name).all();
  data = [];
  for record in results:  # record is a tuple
      tmpObj = {"id":record[0], "name":record[1]};
      data.append(tmpObj);

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term'];
  result = db.session.query(artist.id, artist.name, func.count(show.c.start_time))\
                            .outerjoin(show) \
                            .filter(func.lower(artist.name).like("%" + func.lower(search_term) + "%")) \
                            .filter((show.c.start_time >= postgres_timeStamp_format(datetime.now())) | (show.c.start_time == None)) \
                            .group_by(artist.id, artist.name)\
                            .all();

  response = {'count':len(result), "data":[]};
  for record in result:
      tmpObj = {"id":record[0], "name":record[1], "num_upcoming_shows":record[2]};
      response['data'].append(tmpObj);


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  """
    3 queries to the data base
      - get the artist
      - get past shows
      - get upcomming shows
      -** get genres -- but this one was loaded with the artist query.
  """

  # get the artist
  artistObj = db.session.query(artist).get(artist_id);
  artistId = artistObj.id;

  """
  join shows with artist_id of the current artist id 
  with the venue table to get the venue data that the artist performed at.
  """
  past_showsOfCurArtist = db.session.query(show.c.start_time, venue.id, venue.name, venue.image_link)\
                                            .join(venue)\
                                            .filter(show.c.start_time < postgres_timeStamp_format(datetime.now()))\
                                            .filter(show.c.artist_id == artistId)\
                                           .all();

  upcomming_showsOfCurArtist = db.session.query(show.c.start_time, venue.id, venue.name, venue.image_link)\
                                            .join(venue)\
                                            .filter(show.c.start_time >= postgres_timeStamp_format(datetime.now()))\
                                            .filter(show.c.artist_id == artistId)\
                                           .all();
  genresList = artistObj.genres;

  genres = [];
  for genreObj in genresList:
      genres.append(genreObj.name);

  data={
    "id": artistId,
    "name": artistObj.name,
    "genres": genres,
    "city": artistObj.city,
    "state": artistObj.state,
    "phone": artistObj.phone,
    "website": artistObj.website_link,
    "facebook_link": artistObj.facebook_link,
    "seeking_venue": artistObj.seeking_venue,
    "seeking_description": artistObj.seeking_description,
    "image_link": artistObj.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": len(past_showsOfCurArtist),
    "upcoming_shows_count": len(upcomming_showsOfCurArtist),
  }
  # assign past shows.
  for record in past_showsOfCurArtist:
      tmpObj = {"start_time":postgres_timeStamp_format(record[0]),
                "venue_id":record[1], "venue_name":record[2],
                  "image_link":record[3]};
      data['past_shows'].append(tmpObj);

  # assign upcomming shows.
  for record in upcomming_showsOfCurArtist:
      tmpObj = {"start_time":postgres_timeStamp_format(record[0]),
                "venue_id":record[1], "venue_name":record[2],
                  "image_link":record[3]};
      data['upcoming_shows'].append(tmpObj);

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # get the artist
  artistObj = db.session.query(artist).get(artist_id);
  genresList = artistObj.genres; # joined loading

  genres = [];
  for record in genresList:
    genres.append(record.name)

  form = ArtistForm()
  data={
    "id": artistObj.id,
    "name": artistObj.name,
    "genres": genres,
    "city": artistObj.city,
    "state": artistObj.state,
    "phone": artistObj.phone,
    "website": artistObj.website_link,
    "facebook_link": artistObj.facebook_link,
    "seeking_venue": artistObj.seeking_venue,
    "seeking_description": artistObj.seeking_description,
    "image_link": artistObj.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  """
  # we can't do form validation here as the edit form
  # miss some required data and violate some constraints
  submit_form = ArtistForm();
  if not submit_form.validate_on_submit():
      print("not a valid form -- edit artist");
      return render_template('forms/edit_artist.html', form=submit_form, artist={"id":artistObj.id, "name":artistObj.name});
  """

  error_happens = False;
  genresIds = request.form.getlist('genres');

  form = request.form.to_dict();
  try:
    artistObj = db.session.query(artist).get(artist_id);
    # delete old genres
    artistObj.genres.clear();
    """
    flush to avoid the duplicate key error 
    if the used choosed the same genres as before.
    """
    db.session.flush();

    # edit artist
    artistObj.name = form['name'];
    artistObj.city = form['city'];
    artistObj.state = form['state'];
    artistObj.phone = form['phone'];
    artistObj.facebook_link = form['facebook_link'];

    # add new genres
    for genreId in genresIds:
        statement = artist_genre.insert().values(artist_id=artist_id, genre_id=genreId);
        db.session.execute(statement);

    db.session.commit();
    print("edited successfuly");
  except:
    print("error happens");
    error_happens = True;
    db.session.rollback();
  finally:
    db.session.close();

  if error_happens:
    flash("server error please come back later -- data base is not connected")
    return redirect(url_for('edit_artist', artist_id=artist_id));
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  # get the artist
  venueObj = db.session.query(venue).get(venue_id);
  genresList = venueObj.genres; # joined loading

  genres = [];
  for record in genresList:
    genres.append(record.name)

  form = VenueForm()
  data={
    "id": venueObj.id,
    "name": venueObj.name,
    "genres": genres,
    "address": venueObj.address,
    "city": venueObj.city,
    "state": venueObj.state,
    "phone": venueObj.phone,
    "website": venueObj.website_link,
    "facebook_link": venueObj.facebook_link,
    "seeking_talent": venueObj.seeking_talent,
    "seeking_description": venueObj.seeking_description,
    "image_link": venueObj.image_link
  }
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error_happens = False;
  genresIds = request.form.getlist('genres');

  form = request.form.to_dict();

  try:
    venueObj = db.session.query(venue).get(venue_id);
    # delete old genres
    venueObj.genres.clear();
    db.session.flush();
    # edit artist
    venueObj.name = form['name'];
    venueObj.city = form['city'];
    venueObj.state = form['state'];
    venueObj.address = form['address'];
    venueObj.phone = form['phone'];
    venueObj.facebook_link = form['facebook_link'];
    # add new genres
    print("genres" , venueObj.genres);
    for genreId in genresIds:
      statement = genre_venue.insert().values(venue_id=venue_id, genre_id=genreId);
      db.session.execute(statement);

    db.session.commit();
    print("edited successfuly");
  except Exception as err:
    print("error happens");
    error_happens = True;
    db.session.rollback();
  finally:
    db.session.close();

  if error_happens:
    return redirect(url_for('edit_venue', venue_id=venue_id));
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()  # class with built in functions that will do the checking for me.
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  submit_form = ArtistForm(); # this is supposed to hold the data
  if not submit_form.validate_on_submit():
        print("error happens");
        return render_template('forms/new_artist.html', form=submit_form);

  seeking = False;
  seeking_description = "";

  form = request.form.to_dict();
  if "seeking" in form:
      seeking = True;
      seeking_description = form['seeking_description'];

  newArtist = artist(name=form['name'], city=form['city'], state=form['state'],
                      phone=form['phone'], image_link = form['image_link'],
                     facebook_link = form['facebook_link'], website_link=form['website_link'],
                     seeking_venue = seeking);

  genres  = request.form.getlist('genres');

  if seeking:
    newArtist.seeking_description = seeking_description;

  try:
      db.session.add(newArtist);
      db.session.flush();
      artistId = newArtist.id;
      # add genres
      for genId in genres:
        """
        I didn't do it in this way as I can't do this for 
        genres that are alwready exist 
        tmpGenre = genre(id=genId, name='ahmed');
        newArtist.genres.append(tmpGenre);
        """
        statement = artist_genre.insert().values(artist_id = artistId, genre_id = genId);
        db.session.execute(statement);

      db.session.commit();
      print("successful");
      flash('Artist ' + form['name'] + ' was successfully listed!');

  except:
    # in case that there was other operations other than the add
    # in the same session
    db.session.rollback();
    flash('An error occurred. Artist ' + form['name'] + ' could not be listed.')
  finally:
    db.session.close();

  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at shows
  """
    join the 3 tables
    .c here because show is an associative table not a model

    **** I assumed here that shows page will only display the upcoming show.  *****
  """

  results = db.session.query(venue.id, venue.name, artist.id, artist.name, artist.image_link, show.c.start_time)\
                            .join(show, show.c.venue_id == venue.id)\
                            .join(artist, show.c.artist_id == artist.id)\
                            .filter(show.c.start_time >= postgres_timeStamp_format(datetime.now()))\
                            .all();
  data = [];
  for record in results:
      showObj = {"venue_id":record[0], "venue_name":record[1],
                 "artist_id":record[2], "artist_name":record[3], "artist_image_link":record[4],
                  "start_time":postgres_timeStamp_format(record[5])};
      data.append(showObj);

  return render_template('pages/shows.html', shows=data);

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  form = request.form.to_dict();

  try:
    print("in here");
    sqlQuery = show.insert().values(artist_id = form['artist_id'],
                                      venue_id=form['venue_id'],
                                      start_time=form['start_time']);
    db.session.execute(sqlQuery);
    db.session.commit();
    flash('Show was successfully listed!')
  except Exception as err:
    print("error", err);
    db.session.rollback();
    flash('An error occurred. Show could not be listed. -- '
          '1 artist can not perform 2 shows at the same time -- '
          '1 venue can not have 2 shows at the same time ');
  finally:
    db.session.close();

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500



#################################################################################################################

def insert_artist(data):
  newArtist = artist()
  pass
##################################################################################################################

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')



#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:


if __name__ == '__main__':

    app.run(debug=True);



# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


