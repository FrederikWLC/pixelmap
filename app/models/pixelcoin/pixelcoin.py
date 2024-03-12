from app import db, w3, etherscan
import app.funcs as funcs
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from app.models.static.photo import Photo
from app.models.base import Base
from app.models.location_base import LocationBase
from flask import url_for
import app.models as models
import json
import app.funcs as funcs
import math

class PixelCoin(db.Model, Base, LocationBase):

    def __init__(self,address,**kwargs):
        super(PixelCoin, self).__init__(**{k: kwargs[k] for k in kwargs})
        self.address = address
        # do custom initialization here
        for x in range(0,256):
            for y in range(0,256):
                self.pixels.append(Pixel(x=x,y=y))

    id = db.Column(db.Integer, primary_key=True) # DELETE THIS IN FUTURE
    address = db.Column(db.String(42)) # ETH token address
    block = db.Column(db.Integer) # ETH block number
    total_supply = db.Column(db.Integer, default=0) # Total Amount of tokens

    #events = db.relationship(
    #    'Event', lazy='dynamic',
    #    foreign_keys='Event.pixelmapcoin_id', order_by="Event.timestamp", passive_deletes=True)

    pixels = db.relationship(
        'Pixel', backref="pixelcoin", lazy='dynamic',
        foreign_keys='Pixel.pixelcoin_id',order_by="Pixel.x,Pixel.y",passive_deletes=True)

    @property
    def href(self):
        return f"https://etherscan.io/address/{self.address}"

    def __repr__(self):
        return "<PixelCoin {}>".format(self.address)

class Pixel(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, primary_key=True) 
    y = db.Column(db.Integer, primary_key=True) 



