--
-- DROP EXISTING TABLES
--
DROP TABLE users;
DROP TABLE users_tags;
DROP TABLE tags;
DROP TABLE tags_tagsgroups;
DROP TABLE taggroups;
DROP TABLE users_badges;
DROP TABLE badges;
DROP TABLE geolocation;
DROP TABLE meeting_requests;
DROP TABLE privatechats;
DROP TABLE privatechats_messages;
DROP TABLE publicchats_messages;

--
-- USERS DESCRIPTION
--
CREATE TABLE users (
    id serial8,
    firstname varchar(127),
    lastname varchar(127),
    pseudo varchar(63),
    email varchar(255),
    md5_pass varchar(32),
    photo_b64 text,
    created_at timestamp,
    last_accessed_at timestamp,
    lon float4, 
    lat float4, 
    connected boolean,
    gcm_reg_id varchar(4096),
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

-- Joining table between users & tags
CREATE TABLE users_tags (
    id serial8,
    user_id bigint,
    tag_id int,
    added_at timestamp,
    CONSTRAINT users_tags_pkey PRIMARY KEY (id)
);

CREATE TABLE tags (
    id serial4,
    name varchar(255),
    description varchar(500),
    popularity bigint,
    CONSTRAINT tags_pkey PRIMARY KEY (id)
);

-- Joining table between tags & taggroups
CREATE TABLE tags_taggroups (
    id serial8,
    tag_id int,
    taggroup_id int,
    CONSTRAINT tags_taggroups_pkey PRIMARY KEY (id)
);

CREATE TABLE taggroups (
    id serial4,
    name varchar(255),
    description varchar(500),
    popularity bigint,
    CONSTRAINT taggroups_pkey PRIMARY KEY (id)
);

-- Joining table between users & badges
CREATE TABLE users_badges (
    id serial8,
    user_id bigint,
    badge_id int,
    earned_at timestamp,
    CONSTRAINT users_badges_pkey PRIMARY KEY (id)
);

CREATE TABLE badges (
    id serial4,
    name varchar(100),
    description varchar(500),
    icon_b64 text,
    created_at timestamp,
    last_earned_at timestamp,
    popularity bigint,
    min_interactions int,
    CONSTRAINT badges_pkey PRIMARY KEY (id)
);

--
-- OTHER TABLES
--
CREATE TABLE geolocation (
    id serial8,
    user_id bigint,
    lon float4,
    lat float4,
    created_at timestamp,
    CONSTRAINT geolocation_pkey PRIMARY KEY (id)
);

CREATE TABLE meeting_requests (
    id serial8,
    sent_at timestamp,
    responded_at timestamp,
    sender_id bigint,
    receiver_id bigint,
    accepted boolean,
    sender_lon float4,
    sender_lat float4,
    receiver_lon float4,
    receiver_lat float4,
    CONSTRAINT meeting_requests_pkey PRIMARY KEY (id)
);


-- #############################################################################
-- PRIVATE CHAT
-- ############################################################################

-- Here we denormalize a little, as we could guess started_at & ended_at
CREATE TABLE privatechats (
    id serial8,
    started_at timestamp,
    ended_at timestamp,
    CONSTRAINT privatechats_pkey PRIMARY KEY (id)
);

-- if we want to have a variable number of users participating to a chat, we
-- need this kind of structure
-- Joining table between privatechats & users
CREATE TABLE privatechats_users (
    id serial8,
    privatechat_id bigint,
    user_id bigint,
    invited_by bigint,  -- -1 for the user starting the conversation
    joined_at timestamp,
    left_at timestamp,
    CONSTRAINT privatechats_users_pkey PRIMARY KEY (id) 
);

-- Each message can only belong to one privatechat
-- Not completely normalized because we should store geolocation infos
-- in the special geolocation table
CREATE TABLE privatechats_messages (
    id serial8,
    privatechat_id bigint,
    sender_id bigint,
    content text,
    created_at timestamp,
    lat float4,
    lon float4,
    CONSTRAINT privatechats_messages_pkey PRIMARY KEY (id)
);

-- ############################################################################
-- PUBLIC CHAT
-- ############################################################################

--
CREATE TABLE publicchats_messages (
    id serial8,
    sender_id bigint,
    content text,
    created_at timestamp,
    lat float4,
    lon float4,
    lat_speed float4,
    lon_speed float4,
    CONSTRAINT publicchat_messages_pkey PRIMARY KEY (id)
);


