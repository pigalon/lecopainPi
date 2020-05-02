
CREATE TABLE "users" ( `id` INTEGER NOT NULL UNIQUE, `username` TEXT, `password` TEXT, `email` TEXT, `joined_at` DATETIME, `is_admin` INTEGER, PRIMARY KEY(`id`) )