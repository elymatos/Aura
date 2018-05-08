CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 88dbfc5daf2e

CREATE TABLE roles (
    id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    description VARCHAR, 
    PRIMARY KEY (id), 
    UNIQUE (name)
);

CREATE TABLE users (
    id INTEGER NOT NULL, 
    username VARCHAR NOT NULL, 
    password VARCHAR NOT NULL, 
    active BOOLEAN, 
    PRIMARY KEY (id), 
    UNIQUE (username), 
    CHECK (active IN (0, 1))
);

CREATE TABLE roles_users (
    user_id INTEGER NOT NULL, 
    role_id INTEGER NOT NULL, 
    PRIMARY KEY (user_id, role_id), 
    FOREIGN KEY(role_id) REFERENCES roles (id), 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

INSERT INTO alembic_version (version_num) VALUES ('88dbfc5daf2e');

