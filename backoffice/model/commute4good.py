# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

import config


Base = declarative_base()
metadata = Base.metadata

def date_tostring(date):
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    try:
        s = date.strftime(DATE_FORMAT)
    except Exception, e:
        s = None
    return s

class Badge(Base):
    __tablename__ = u'badges'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    icon_b64 = Column(Text)
    created_at = Column(DateTime)
    last_earned_at = Column(DateTime)
    popularity = Column(BigInteger)
    min_interactions = Column(Integer)
 
    def to_dict(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon_b64": self.icon_b64,
            "created_at": date_tostring(self.created_at),
            "last_earned_at": date_tostring(self.last_earned_at),
            "popularity": self.popularity,
            "min_interactions": self.min_interactions,
        }
        return dict

class Geolocation(Base):
    __tablename__ = u'geolocation'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    lon = Column(Float)
    lat = Column(Float)
    created_at = Column(DateTime)

    def to_dict(self):
        dict = {
            "id": self.id,
            "user_id": self.user_id,
            "lon": self.lon ,
            "lat": self.lat,
            "created_at ": date_tostring(self.created_at)
        }
        return dict


class MeetingRequest(Base):
    __tablename__ = u'meeting_requests'

    id = Column(BigInteger, primary_key=True)
    sent_at = Column(DateTime)
    responded_at = Column(DateTime)
    sender_id = Column(BigInteger)
    receiver_id = Column(BigInteger)
    accepted = Column(Boolean)
    sender_lon = Column(Float)
    sender_lat = Column(Float)
    receiver_lon = Column(Float)
    receiver_lat = Column(Float)


class Privatechat(Base):
    __tablename__ = u'privatechats'

    id = Column(BigInteger, primary_key=True)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)


class PrivatechatsMessage(Base):
    __tablename__ = u'privatechats_messages'

    id = Column(BigInteger, primary_key=True)
    privatechat_id = Column(BigInteger)
    sender_id = Column(BigInteger)
    content = Column(Text)
    created_at = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)

    def to_dict(self):
        dict = {
            "id": self.id,
            "privatechat_id":   self.privatechat_id,
            "sender_id": self.sender_id,
            "content": self.content,
            "created_at ": date_tostring(self.created_at),
            "lat": self.lat,
            "lon": self.lon
        }
        return dict


class PrivatechatsUser(Base):
    __tablename__ = u'privatechats_users'

    id = Column(BigInteger, primary_key=True)
    privatechat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    invited_by = Column(BigInteger)
    joined_at = Column(DateTime)
    left_at = Column(DateTime)


class PublicchatsMessage(Base):
    __tablename__ = u'publicchats_messages'

    id = Column(BigInteger, primary_key=True)
    sender_id = Column(BigInteger)
    content = Column(Text)
    created_at = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    lat_speed = Column(Float)
    lon_speed = Column(Float)


    def to_dict(self):
        dict = {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "created_at ": date_tostring(self.created_at),
            "lat": self.lat,
            "lon": self.lon,
            "lat_speed": self.lat_speed,
            "lon_speed": self.lon_speed
        }
        return dict

class Taggroup(Base):
    __tablename__ = u'taggroups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(500))
    popularity = Column(BigInteger)


class Tag(Base):
    __tablename__ = u'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(500))
    popularity = Column(BigInteger)

    def to_dict(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "popularity": self.popularity
        }
        return dict

class TagsTaggroup(Base):
    __tablename__ = u'tags_taggroups'

    id = Column(BigInteger, primary_key=True)
    tag_id = Column(Integer)
    taggroup_id = Column(Integer)


class User(Base):
    __tablename__ = u'users'

    id = Column(BigInteger, primary_key=True)
    firstname = Column(String(127))
    lastname = Column(String(127))
    pseudo = Column(String(63))
    email = Column(String(255))
    md5_pass = Column(String(32))
    photo_b64 = Column(Text)
    created_at = Column(DateTime)
    last_accessed_at = Column(DateTime)
    lon = Column(Float)
    lat = Column(Float)
    connected = Column(Boolean)
    gcm_reg_id = Column(String(4096))

    def to_dict(self):
        """
        return every fields except 'md5_pass'
        """
        dict = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "pseudo": self.pseudo,
            "email": self.email,
            "photo_b64": self.photo_b64,
            "created_at": date_tostring(self.created_at),
            "last_accessed_at": date_tostring(self.last_accessed_at),
            "lon": self.lon,
            "lat": self.lat,
            "connected": self.connected,
            "gcm_reg_id": self.gcm_reg_id
        }
        return dict

class UsersBadge(Base):
    __tablename__ = u'users_badges'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    badge_id = Column(Integer)
    earned_at = Column(DateTime)


class UsersTag(Base):
    __tablename__ = u'users_tags'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    tag_id = Column(Integer)
    added_at = Column(DateTime)
