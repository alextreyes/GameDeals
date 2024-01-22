-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/TIBpqQ
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "user" (
    "id" int   NOT NULL,
    "username" text  NOT NULL, 
    "password" text   NOT NULL,
    "profile_pic" text   NOT NULL,
    "user_list" int   NOT NULL,
    "liked_lists" int   NOT NULL,
    "likes" int   NOT NULL,
    CONSTRAINT "pk_user" PRIMARY KEY ("id")
);

CREATE TABLE "userlist" (
    "id" int   NOT NULL,
    "user_id" int   NOT NULL,
    "game_id" int   NOT NULL,
    "likes" int   NOT NULL,
    CONSTRAINT "pk_userlist" PRIMARY KEY ("id")
);

CREATE TABLE "game" (
    "id" int   NOT NULL,
    "name" text   NOT NULL,
    "tags" text   NOT NULL,
    "current_price" int   NOT NULL,
    CONSTRAINT "pk_game" PRIMARY KEY ("id")
);

CREATE TABLE "likes" (
    "id" int   NOT NULL,
    "user_id" int   NOT NULL,
    "list_id" int   NOT NULL,
    CONSTRAINT "pk_likes" PRIMARY KEY ("id")
);

ALTER TABLE "user" ADD CONSTRAINT "fk_user_userlist" FOREIGN KEY ("user_list")
REFERENCES "userlist" ("id");

ALTER TABLE "userlist" ADD CONSTRAINT "fk_userlist_user_id" FOREIGN KEY ("user_id")
REFERENCES "user" ("id");

ALTER TABLE "userlist" ADD CONSTRAINT "fk_userlist_game_id" FOREIGN KEY ("game_id")
REFERENCES "game" ("id");

ALTER TABLE "likes" ADD CONSTRAINT "fk_likes_user_id" FOREIGN KEY ("user_id")
REFERENCES "user" ("id");

ALTER TABLE "likes" ADD CONSTRAINT "fk_likes_list_id" FOREIGN KEY ("list_id")
REFERENCES "userlist" ("id");

CREATE INDEX "idx_user_username"
ON "user" ("username");


