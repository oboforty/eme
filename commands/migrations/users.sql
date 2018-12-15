CREATE TABLE IF NOT EXISTS userspaces (
    "uid" uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    "created_at" timestamp NOT NULL DEFAULT (now() AT TIME ZONE 'UTC'),
    "email" character varying(40) NOT NULL,
    "salt" character varying(128) NOT NULL,
    "token" character varying(128) NOT NULL,
    "password" character varying(128) NOT NULL
);
