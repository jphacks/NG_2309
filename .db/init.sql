CREATE DATABASE if not exists user_data;
USE user_data;
CREATE TABLE user_list(
    user_name TEXT,
    commit_num INT,
    percent FLOAT);