# -*- coding: utf-8 -*-
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import config


Base = declarative_base()
metadata = Base.metadata


class Badge(Base):
    __tablename__ = u'badges'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(500))
    icon_path = Column(String(255))
    created_at = Column(DateTime)
    last_earned_at = Column(DateTime)
    popularity = Column(BigInteger)
    min_interactions = Column(Integer)


class Geolocation(Base):
    __tablename__ = u'geolocation'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    lon = Column(Float)
    lat = Column(Float)
    created_at = Column(DateTime)


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
    md5_hash = Column(String(64))
    photo_path = Column(String(255))
    created_at = Column(DateTime)
    last_accessed_at = Column(DateTime)
    lon = Column(Float)
    lat = Column(Float)
    connected = Column(Boolean)


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
