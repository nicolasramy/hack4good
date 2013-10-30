--
-- TO DROP ALL TABLES IN commute4good DATABASE, EXECUTE NEXT COMMAND IN A SHELL
-- (ADD RELEVENT PATH IN FRONT OF SQL FILE IF NECESSARY)
-- psql -h localhost -p 5432 -U postgres -d commute4good -f drop_all_tables_commute_db.sql
--
DROP TABLE users;
DROP TABLE users_tags;
DROP TABLE tags;
DROP TABLE tags_taggroups;
DROP TABLE taggroups;
DROP TABLE users_badges;
DROP TABLE badges;
DROP TABLE geolocation;
DROP TABLE meeting_requests;
DROP TABLE privatechats;
DROP TABLE privatechats_messages;
DROP TABLE privatechats_users;
DROP TABLE publicchats_messages;


