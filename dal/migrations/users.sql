CREATE TABLE users (
    "uid" integer NOT NULL,
    "email" character varying(40),
    "password" character varying(128),
    "salt" character varying(128),
    "token" character varying(128)
);
