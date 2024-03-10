CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    profile_pic TEXT DEFAULT '/static/images/default-pic.png'
);

CREATE TABLE user_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    list_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE user_list_games (
    list_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    name VARCHAR(128),
    thumbnail VARCHAR(256),
    webpage VARCHAR(512),
    metacritic VARCHAR(512),
    rating VARCHAR(512),
    PRIMARY KEY (list_id, game_id),
    FOREIGN KEY (list_id) REFERENCES user_lists(id) ON DELETE CASCADE
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    list_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (list_id) REFERENCES user_lists(id) ON DELETE CASCADE
);
