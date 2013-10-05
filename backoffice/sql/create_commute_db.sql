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

CREATE TABLE badges (
    id serial4,
    name varchar(100),
    description varchar(500),
    icon_path varchar(255),
    created_at timestamp,
    last_earned_at timestamp,
    popularity bigint,
    min_interactions int,
    CONSTRAINT badges_pkey PRIMARY KEY (id)
);

CREATE TABLE tags (
    id serial4,
    name varchar(255),
    description varchar(500),
    popularity bigint,
    CONSTRAINT tags_pkey PRIMARY KEY (id)
);

CREATE TABLE taggroups (
    id serial4,
    name varchar(255),
    description varchar(500),
    popularity bigint,
    CONSTRAINT taggroups_pkey PRIMARY KEY (id)
);

CREATE TABLE users (
    id serial8,
    firstname varchar(127),
    lastname varchar(127),
    pseudo varchar(63),
    email varchar(255),
    md5_hash varchar(64),
    photo_path varchar(255),
    created_at timestamp,
    last_accessed_at timestamp,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

CREATE TABLE users_tags (
    id serial8,
    user_id bigint,
    tag_id int,
    added_at timestamp,
    CONSTRAINT users_tags_pkey PRIMARY KEY (id)
);

CREATE TABLE users_badges (
    id serial8,
    user_id bigint,
    badge_id int,
    earned_at timestamp,
    CONSTRAINT users_badges_pkey PRIMARY KEY (id)
);

CREATE TABLE tags_taggroups (
    id serial8,
    tag_id int,
    taggroup_id int,
    CONSTRAINT tags_taggroups_pkey PRIMARY KEY (id)
);
