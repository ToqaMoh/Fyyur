from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

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
  start_time = db.Column(db.DateTime, nullable=False)
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

#   def getVenuePastUpcomingShows(self):

#     pshows = []
#     upcshows = []

#     for show in self.shows:
#       if show.start_time <= datetime.now():
#         pshows.append(show)
#       elif show.start_time > datetime.now():
#         upcshows.append(show)
       
#     self.past_shows = pshows
#     self.past_shows_count = len(self.past_shows)
#     self.upcoming_shows = upcshows
#     self.upcoming_shows_count = len(self.upcoming_shows)
    
#     return "Done"



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

  
#   def getArtistPastUpcomingShows(self):

#     artistpshows = []
#     artistupcshows = []

#     for show in self.shows:
#       if show.start_time <= datetime.now():
#         artistpshows.append(show)
#       elif show.start_time > datetime.now():
#         artistupcshows.append(show)
       
#     self.past_shows = artistpshows
#     self.past_shows_count = len(self.past_shows)
#     self.upcoming_shows = artistupcshows
#     self.upcoming_shows_count = len(self.upcoming_shows)
    
#     return "Done"



    # TODO: implement any missing fields, as a database migration using Flask-Migrate ** DONE **


  
  def artistDict(self):
    return(
      {
        "id": self.id, "name": self.name, "city": self.city, "state": self.state, "phone": self.phone, "website": self.website, "image_link": self.image_link, "facebook_link": self.facebook_link, "genres": self.genres, "seeking_venue": self.seeking_venue, "seeking_description": self.seeking_description, "shows": [ Shows.showDict(show) for show in self.shows ]
      }
    )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate ** DONE **

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. ** DONE **
