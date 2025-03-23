from app import db
import datetime
from sqlalchemy.dialects.postgresql import JSONB

# define a itinerary model
class Itinerary(db.Model):
    __tablename__ = 'itineraries'
    
    id = db.Column(db.Integer, primary_key=True)
    short_URL = db.Column(db.String(8), unique=True)
    data = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # convert model instance into a dictionary for returning json
    def to_dict(self):
        return {
            'short_URL': self.short_URL,
            'data': self.data,
            'created_at': self.created_at
        }
    
class TripRequest(db.Model):
    __tablename__ = 'trip_requests'

    id = db.Column(db.Integer, primary_key=True)
    short_ID = db.Column(db.String(8), unique=True)
    data = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def to_dict(self):
        return {
            'short_ID': self.short_ID,
            'data': self.data,
            'created_at': self.created_at
        }