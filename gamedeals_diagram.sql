
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profile_pic TEXT
);

CREATE TABLE user_lists (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    list_name TEXT NOT NULL,
    CONSTRAINT fk_user_lists_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE user_list_games (
    list_id INT NOT NULL,
    game_id INT,
    PRIMARY KEY (list_id, game_id),
    CONSTRAINT fk_user_list_games_list_id FOREIGN KEY (list_id) REFERENCES user_lists(id) ON DELETE CASCADE
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    list_id INT NOT NULL,
    CONSTRAINT fk_likes_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_likes_list_id FOREIGN KEY (list_id) REFERENCES user_lists(id) ON DELETE CASCADE
);

CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_user_lists_user_id ON user_lists (user_id);



