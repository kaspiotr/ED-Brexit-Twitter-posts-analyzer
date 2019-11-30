DROP TABLE IF EXISTS tweets CASCADE;

CREATE TABLE tweets (
    id BIGINT,
    userId BIGINT REFERENCES users(id),
    fullText VARCHAR(1680),
    createdAt TIMESTAMP,
    inReplyToTweetId BIGINT,
    inReplyToUserId BIGINT,
    sentiment DOUBLE PRECISION,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id BIGINT,
    name VARCHAR(1680),
    screenName VARCHAR(1680),
    location VARCHAR(1680),
    description VARCHAR (1680),
    language VARCHAR(1680),
    followersNumber INT,
    friendsNumber INT,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS hashtags CASCADE;

CREATE TABLE hashtags (
    id BIGSERIAL,
    name VARCHAR(280),
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS tweetshashtags CASCADE;

CREATE TABLE tweetsHashtags (
    hashtagId BIGINT REFERENCES hashtags(id),
    tweetId BIGINT REFERENCES tweets(id),
    PRIMARY KEY (hashtagId, tweetId)
);

DROP TABLE IF EXISTS likes CASCADE;

CREATE TABLE likes (
    tweetId BIGINT REFERENCES tweets(id),
    userId BIGINT,
    PRIMARY KEY (tweetId, userId)
);

DROP TABLE IF EXISTS "comments" CASCADE;

CREATE TABLE comments (
    tweetId BIGINT REFERENCES tweets(id),
    userId BIGINT,
    PRIMARY KEY (tweetId, userId)
);

DROP TABLE IF EXISTS mentions CASCADE;

CREATE TABLE mentions (
    tweetId BIGINT REFERENCES tweets(id),
    userId BIGINT,
    PRIMARY KEY (tweetId, userId)
);

DROP TABLE IF EXISTS retweets CASCADE;

CREATE TABLE retweets (
    tweetId BIGINT REFERENCES tweets(id),
    userId BIGINT,
    PRIMARY KEY (tweetId, userId)
);