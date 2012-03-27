#from sqlalchemy.orm import relationship, backref, object_mapper
from sqlalchemy import Column, Integer, BigInteger, String, schema
#from sqlalchemy import ForeignKey, DateTime, Boolean, Text, Float
#from sqlalchemy.exc import IntegrityError
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.schema import ForeignKeyConstraint

from nova.db.sqlalchemy import session
from nova.db.sqlalchemy import models

class Region(models.BASE, models.NovaBase):
    """Represents regions."""

    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
