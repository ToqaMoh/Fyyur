#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
#
import json
import dateutil.parser
import babel
import datetime
import time
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import re
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database  ** DONE **

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Cities(db.Model):
  __tablename__ = 'cities'
  id = db.Column(db.Integer, nullable=False, primary_key=True)
  cityname = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  venues = db.relationship('Venues', backref='venues_city', lazy=True)

  def __init__(self, cityname, state, venues):
    self.cityname = cityname
    self.state = state
    self.venues = venues

  def cityDict(self):
    return(
      {
        "id": self.id, "cityname": self.cityname, "state": self.state , "venues": [ Venues.venueDict(venue) for venue in self.venues ]
      }
    ) 


class Shows(db.Model):
  __tablename__ = 'shows'
  id = db.Column(db.Integer, nullable=False, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, default=datetime.now().isoformat())
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)
  venue_name = db.Column(db.String, nullable=False)
  venue_image_link = db.Column(db.String(500))
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  artist_name = db.Column(db.String, nullable=False)
  artist_image_link = db.Column(db.String(500))

  def __init__(self, start_time, venue_id, venue_name, venue_image_link, artist_id, artist_name, artist_image_link):
    self.start_time = start_time
    self.venue_id = venue_id
    self.venue_name = venue_name
    self.venue_image_link = venue_image_link
    self.artist_id = artist_id
    self.artist_name = artist_name
    self.artist_image_link = artist_image_link

  def showDict(self):
    return(
      {
        "id": self.id, "start_time": self.start_time, "venue_id": self.venue_id, "venue_name": self.venue_name, "venue_image_link": self.venue_image_link, "artist_id": self.artist_id, "artist_name": self.artist_name, "artist_image_link": self.artist_image_link
      }
    ) 

class Venues(db.Model):
  __tablename__ = 'venues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120), nullable=False)
  state = db.Column(db.String(120), nullable=False)
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()))
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500))
  past_shows = db.Column(db.ARRAY(db.String()))
  upcoming_shows = db.Column(db.ARRAY(db.String()))
  past_shows_count = db.Column(db.Integer)
  upcoming_shows_count = db.Column(db.Integer)
  city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
  shows = db.relationship('Shows', backref='venue_shows', passive_deletes=True, lazy=True) 


  def __init__(self, name, city, state, address, phone, image_link, facebook_link, website, genres, seeking_talent, seeking_description, city_id):
    self.name = name
    self.city = city
    self.state = state
    self.address = address
    self.phone = phone
    self.image_link = image_link
    self.facebook_link = facebook_link
    self.website = website
    self.genres = genres
    self.seeking_talent = seeking_talent
    self.seeking_description = seeking_description
    self.city_id = city_id

  def __repr__(self):
    return f'"id" = {self.id},"name" = {self.name},"city" = {self.city},"state" = {self.state},"address" = {self.address},"phone" = {self.phone},"image_link" = {self.image_link},"facebook_link" = {self.facebook_link},"website" = {self.website},"genres" = {self.genres},"seeking_talent" = {self.seeking_talent},"seeking_description" = {self.seeking_description},"city_id" = {self.city_id}'


  def venueDict(self):
    return(
      {
        "id": self.id, "name": self.name, "city": self.city, "state": self.state, "address": self.address, "phone": self.phone, "image_link": self.image_link, "facebook_link": self.facebook_link, "website": self.website, "genres": self.genres, "seeking_talent": self.seeking_talent, "seeking_description": self.seeking_description, "city_id": self.city_id, "shows": [ Shows.showDict(show) for show in self.shows ]
      }
    )

  def getVenuePastUpcomingShows(self):

    pshows = []
    upcshows = []

    for show in self.shows:
      if show.start_time <= datetime.now():
        pshows.append(show)
      elif show.start_time > datetime.now():
        upcshows.append(show)
       
    self.past_shows = pshows
    self.past_shows_count = len(self.past_shows)
    self.upcoming_shows = upcshows
    self.upcoming_shows_count = len(self.upcoming_shows)
    
    return "Done"



    # TODO: implement any missing fields, as a database migration using Flask-Migrate ** DONE **

class Artists(db.Model):
  __tablename__ = 'artists'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  website = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String()))
  seeking_venue = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500))
  past_shows = db.Column(db.ARRAY(db.String()))
  upcoming_shows = db.Column(db.ARRAY(db.String()))
  past_shows_count = db.Column(db.Integer)
  upcoming_shows_count = db.Column(db.Integer)
  shows = db.relationship('Shows', backref='artist_shows', lazy=True)


  def __init__(self, name, city, state, phone, website, image_link, facebook_link, genres, seeking_venue, seeking_description):
    self.name = name
    self.city = city
    self.state = state
    self.phone = phone
    self.website = website
    self.image_link = image_link
    self.facebook_link = facebook_link
    self.genres = genres
    self.seeking_venue = seeking_venue
    self.seeking_description = seeking_description

  def __repr__(self):
    return f'< Artist: {self.id}) {self.name} >'

  
  def getArtistPastUpcomingShows(self):

    artistpshows = []
    artistupcshows = []

    for show in self.shows:
      if show.start_time <= datetime.now():
        artistpshows.append(show)
      elif show.start_time > datetime.now():
        artistupcshows.append(show)
       
    self.past_shows = artistpshows
    self.past_shows_count = len(self.past_shows)
    self.upcoming_shows = artistupcshows
    self.upcoming_shows_count = len(self.upcoming_shows)
    
    return "Done"



    # TODO: implement any missing fields, as a database migration using Flask-Migrate ** DONE **


  
  def artistDict(self):
    return(
      {
        "id": self.id, "name": self.name, "city": self.city, "state": self.state, "phone": self.phone, "website": self.website, "image_link": self.image_link, "facebook_link": self.facebook_link, "genres": self.genres, "seeking_venue": self.seeking_venue, "seeking_description": self.seeking_description, "shows": [ Shows.showDict(show) for show in self.shows ]
      }
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate ** DONE **

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. ** DONE **

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  #date = dateutil.parser.parse(value)
  print(value)
  if format == 'full':
      format="EEEE MMMM, dd, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(value, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


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
  # TODO: replace with real venues data. ** DONE **
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]

  allData = Cities.query.order_by('id').all()
  
  return render_template('pages/venues.html', areas=allData)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. ** DONE **
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }

  search_term=request.form['search_term']

  return render_template('pages/search_venues.html', search_term=search_term, results=Venues.query.filter(Venues.name.ilike('%{}%'.format(search_term))).all())

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id ** DONE **
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

  data = Venues.query.get(venue_id)
  Venues.getVenuePastUpcomingShows(data)
  print(data.venueDict())

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead ** DONE **
  # TODO: modify data to be the data object returned from db insertion ** DONE **

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  genres = request.form.getlist('genres')
  seeking_description = request.form['seeking_description']
  website = request.form['website']

  form = VenueForm()
  if form.validate_on_submit():
    try:
      if seeking_description == "":
        seeking_talent = False
      else:
        seeking_talent = True
      cityResult = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
      if cityResult == None:
        try:
          newCity = Cities(city, state, [])
          print(newCity.cityDict())
          db.session.add(newCity)
          db.session.commit()
          getCity = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
          city_id = getCity.id
          newVenue = Venues(name, city, state, address, phone, image_link, facebook_link, website, genres, seeking_talent, seeking_description, city_id)
          db.session.add(newVenue)
          db.session.commit() 
          data = newVenue.venueDict()
          print(data)
        except:
          db.session.rollback()
          print(sys.exc_info)
        finally:
          db.session.close()  
      else:
        print(cityResult.cityDict())
        try:
          city_id = cityResult.id
          newVenue = Venues(name, city, state, address, phone, image_link, facebook_link, website, genres, seeking_talent, seeking_description, city_id)
          db.session.add(newVenue)
          db.session.commit()
          data = newVenue.venueDict()
          print(data)
        except:
          db.session.rollback()
          print(sys.exc_info)
        finally:
          db.session.close()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      print(sys.exc_info)
      flash('Something went wrong!')
  else:
    return render_template('forms/new_venue.html', form=form)


  
    

  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using ** DONE **
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  try:
    Venues.query.filter(Venues.id==venue_id).delete()
    db.session.commit()
    flash('The Venue was successfully Deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()

  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database ** DONE **
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]

  allData = Artists.query.order_by('id').all()

  return render_template('pages/artists.html', artists=allData)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. ** DONE **
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }

  search_term=request.form['search_term']

  return render_template('pages/search_artists.html', search_term=search_term, results=Artists.query.filter(Artists.name.ilike('%{}%'.format(search_term))).all())

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id ** DONE **
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

  data = Artists.query.get(artist_id)
  Artists.getArtistPastUpcomingShows(data)
  print(data.artistDict())

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id> ** DONE **

  data = Artists.query.get(artist_id)
  form = ArtistForm(obj=data)

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing ** DONE **
  # artist record with ID <artist_id> using the new attributes

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  website = request.form['website']
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  genres = request.form.getlist('genres')
  seeking_description = request.form['seeking_description']
  if seeking_description == "":
    seeking_venue = False
  else:
    seeking_venue = True

  try:
    cityResult = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
    if cityResult == None:
      try:
        newCity = Cities(city, state, [])
        print(newCity.cityDict())
        db.session.add(newCity)
        db.session.commit()
        Edit_Artist = Artists.query.get(artist_id)
        Edit_Artist.name = name
        Edit_Artist.city = city
        Edit_Artist.state = state
        Edit_Artist.phone = phone
        Edit_Artist.website = website
        Edit_Artist.image_link = image_link
        Edit_Artist.facebook_link = facebook_link
        Edit_Artist.genres = genres
        Edit_Artist.seeking_description = seeking_description
        Edit_Artist.seeking_venue = seeking_venue
        db.session.commit()     
      except:
        db.session.rollback()
        print(sys.exc_info)
      finally:
        db.session.close()  
    else:
      try:
        Edit_Artist = Artists.query.get(artist_id)
        Edit_Artist.name = name
        Edit_Artist.city = city
        Edit_Artist.state = state
        Edit_Artist.phone = phone
        Edit_Artist.website = website
        Edit_Artist.image_link = image_link
        Edit_Artist.facebook_link = facebook_link
        Edit_Artist.genres = genres
        Edit_Artist.seeking_description = seeking_description
        Edit_Artist.seeking_venue = seeking_venue
        db.session.commit()
      except:
        db.session.rollback()
        print("ex")
      finally:
        db.session.close()
    flash('Artist ' + request.form['name'] + ' was successfully Edited!')
  except:
    print(sys.exc_info)
    flash('Something went wrong!')


  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id> ** DONE **

  data = Venues.query.get(venue_id)
  form = VenueForm(obj=data)

  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing  ** DONE **
  # venue record with ID <venue_id> using the new attributes

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  genres = request.form.getlist('genres')
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  website = request.form['website']
  seeking_description = request.form['seeking_description']
  if seeking_description == "":
    seeking_talent = False
  else:
    seeking_talent = True

  try:
    cityResult = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
    if cityResult == None:
      try:
        newCity = Cities(city, state, [])
        print(newCity.cityDict())
        db.session.add(newCity)
        db.session.commit()
        getCity = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
        Edit_Venue = Venues.query.get(venue_id)
        Edit_Venue.name = name
        Edit_Venue.city = city
        Edit_Venue.state = state
        Edit_Venue.address = address
        Edit_Venue.phone = phone
        Edit_Venue.genres = genres
        Edit_Venue.image_link = image_link
        Edit_Venue.facebook_link = facebook_link
        Edit_Venue.website = website
        Edit_Venue.seeking_description = seeking_description
        Edit_Venue.seeking_talent = seeking_talent
        Edit_Venue.city_id = getCity.id
        db.session.commit()     
      except:
        db.session.rollback()
        print(sys.exc_info)
      finally:
        db.session.close()  
    else:
      try:
        city_id = cityResult.id
        Edit_Venue = Venues.query.get(venue_id)
        Edit_Venue.name = name
        Edit_Venue.city = city
        Edit_Venue.state = state
        Edit_Venue.address = address
        Edit_Venue.phone = phone
        Edit_Venue.genres = genres
        Edit_Venue.image_link = image_link
        Edit_Venue.facebook_link = facebook_link
        Edit_Venue.website = website
        Edit_Venue.seeking_description = seeking_description
        Edit_Venue.seeking_talent = seeking_talent
        Edit_Venue.city_id = city_id
        db.session.commit()
      except:
        db.session.rollback()
        print("ex")
      finally:
        db.session.close()
    flash('Venue ' + request.form['name'] + ' was successfully Edited!')
  except:
    print(sys.exc_info)
    flash('Something went wrong!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead ** DONE **
  # TODO: modify data to be the data object returned from db insertion  ** DONE **

  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  website = request.form['website']
  image_link = request.form['image_link']
  facebook_link = request.form['facebook_link']
  genres = request.form.getlist('genres')
  seeking_description = request.form['seeking_description']

  form = ArtistForm()
  if form.validate_on_submit():
    try:
      if seeking_description == "":
        seeking_venue = False
      else:
        seeking_venue = True
      cityResult = Cities.query.filter(Cities.cityname==city, Cities.state==state).first()
      if cityResult == None:
        try:
          newCity = Cities(city, state, [])
          print(newCity.cityDict())
          db.session.add(newCity)
          db.session.commit()
          newArtist = Artists(name, city, state, phone, website, image_link, facebook_link, genres, seeking_venue, seeking_description)
          db.session.add(newArtist)
          db.session.commit()     
          data = newArtist.artistDict()
          print(data)
        except:
          db.session.rollback()
          print(sys.exc_info)
        finally:
          db.session.close()  
      else:
        try:
          newArtist = Artists(name, city, state, phone, website, image_link, facebook_link, genres, seeking_venue, seeking_description)
          print(newArtist.artistDict())
          db.session.add(newArtist)
          db.session.commit()
          data = newArtist.artistDict()
          print(data)
        except:
          db.session.rollback()
          print("ex")
        finally:
          db.session.close()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      return render_template('pages/home.html')

    except:
      print(sys.exc_info)
      # TODO: on unsuccessful db insert, flash an error instead. ** DONE **
      flash('Something went wrong!')
  else:
    return render_template('forms/new_artist.html', form=form)
 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. ** DONE **
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  allData = Shows.query.order_by('id').all()

  return render_template('pages/shows.html', shows=allData)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead  ** DONE **

  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  
  try:
    artist = Artists.query.get(artist_id)
    artist_name = artist.name
    artist_image_link = artist.image_link
    print(artist.artistDict())
  except:
    flash('This Artist Does not exist!')
  
  try:
    venue = Venues.query.get(venue_id)
    venue_name = venue.name
    venue_image_link = venue.image_link
    print(venue.venueDict())
  except:
    flash('This Venue Does not exist!')

  try:
    venue_id = int(venue_id)
    artist_id = int(artist_id)
    newShow = Shows(start_time, venue_id, venue_name, venue_image_link, artist_id, artist_name, artist_image_link)
    print(newShow.showDict())
    db.session.add(newShow)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info)
    # TODO: on unsuccessful db insert, flash an error instead. ** DONE **
    flash('Something went wrong!')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
