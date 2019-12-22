import psycopg2
from collections import namedtuple
from string import Template

EDGE_BASE_ROW = '<edge id="%s" source="%s" target="%s" weight="%s"/>'
NODE_BASE_ROW = '<node id="%s" label="%s" />'
NODE_ATTRIBUTE_BASE_ROW = '<node id="%s" label="%s">\n<attvalues>\n%s\n</attvalues>\n</node>'
ATTVALUE_BASE_ROW = '<attvalue for="%s" value="%s"></attvalue>'
ATTIBUTE_DEFINE_BASE_ROW = '<attribute id="%s" title="%s" type="%s"></attribute>'


def connect_to_database():
    file = open('dbconnectioncredentials', 'r')
    creds_dict = {}
    for line in file:
        credential = line.split("=")
        value = credential[1]
        creds_dict[credential[0]] = value[0:len(value) - 1]
    connection = psycopg2.connect(
        host=creds_dict['SERVER'],
        dbname=creds_dict['DATABASE_NAME'],
        user=creds_dict['USER_NAME'],
        password=creds_dict['PASSWORD'],
        port=creds_dict['PORT']
    )
    return connection


def fill_gephi_file(filename, new_filename, nodes, edges, attributes=None):
    filein = open(filename)
    src = Template(filein.read())
    d = {'attributes_list': attributes, 'node_list': '\n'.join(nodes), 'edge_list': '\n'.join(edges)}
    result = src.substitute(d)
    new_filename_write = open(new_filename, "w")
    new_filename_write.write(result)
    new_filename_write.close()


def create_input_sentiment(nodes, edges, User):
    nodes_str, edges_str = [], []
    attributes_definiton = [ATTIBUTE_DEFINE_BASE_ROW % ('followers_number', 'Followers number', 'int'),
                            ATTIBUTE_DEFINE_BASE_ROW % ('sentiment_average', 'Sentiment', 'float')]

    for node in nodes:
        if isinstance(node, User):
            attributes = [ATTVALUE_BASE_ROW % ('followers_number', node.followers_number),
                          ATTVALUE_BASE_ROW % ('sentiment_average', node.sentiment_average)]
            nodes_str.append(NODE_ATTRIBUTE_BASE_ROW % (node.id, node.name, ("\n".join(attributes))))
        else:
            nodes_str.append(NODE_BASE_ROW % (node.id, node.name))

    for i, edge in enumerate(edges):
        edges_str.append(EDGE_BASE_ROW % (i, edge[0], edge[1], edge[2]))

    return nodes_str, edges_str, attributes_definiton


def create_input(nodes, edges, User):
    nodes_str, edges_str = [], []
    attributes_definiton = [ATTIBUTE_DEFINE_BASE_ROW % ('followers_number', 'Followers number', 'int'),
                            ATTIBUTE_DEFINE_BASE_ROW % ('friends_number', 'Friends number', 'int')]

    for node in nodes:
        if isinstance(node, User):
            attributes = [ATTVALUE_BASE_ROW % ('followers_number', node.followers_number),
                          ATTVALUE_BASE_ROW % ('friends_number', node.friends_number)]
            nodes_str.append(NODE_ATTRIBUTE_BASE_ROW % (node.id, node.name, ("\n".join(attributes))))
        else:
            nodes_str.append(NODE_BASE_ROW % (node.id, node.name))

    for i, edge in enumerate(edges):
        edges_str.append(EDGE_BASE_ROW % (i, edge[0], edge[1], edge[2]))

    return nodes_str, edges_str, attributes_definiton


def retweets(connection):
    SQL_QUERY = "SELECT count(tweetid) AS tweet_counts, retweets.userid, users.screenname, users.followersnumber, users.friendsnumber, tweets.userid, users_mentioning.screenname, users_mentioning.followersnumber, users_mentioning.friendsnumber FROM Retweets " \
                         "INNER JOIN users ON users.id=userid INNER JOIN tweets ON tweets.id=tweetid " \
                         "INNER JOIN users AS users_mentioning ON users_mentioning.id = tweets.userid " \
                         "WHERE users.followersnumber > 1000000 " \
                         "GROUP BY retweets.userid, users.screenname, users.followersnumber, users.friendsnumber, users_mentioning.id, tweets.userid, users_mentioning.screenname, users_mentioning.followersnumber, users_mentioning.friendsnumber " \
                         "ORDER BY tweet_counts DESC " \
                         "LIMIT 200;"

    User = namedtuple("User", 'id name followers_number friends_number')
    nodes, edges = set(), []
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    for i in cursor.fetchall():
        nodes.add(User(i[1], i[2], i[3], i[4]))
        nodes.add(User(i[5], i[6], i[7], i[8]))
        edges.append((i[1], i[5], i[0]))

    nodes_str, edges_str, attributes = create_input(list(nodes), edges, User)

    fill_gephi_file("gephi_raw_file.gexf", "gephi_retweets.gexf",
                    nodes_str, edges_str, attributes)


def mentions(connection):
    SQL_QUERY= "SELECT count(tweetid) AS tweet_counts, mentions.userid, users.screenname, users.followersnumber, users.friendsnumber, tweets.userid, users_mentioning.screenname, users_mentioning.followersnumber, users_mentioning.friendsnumber FROM MENTIONS " \
                          "INNER JOIN users ON users.id=userid INNER JOIN tweets ON tweets.id=tweetid " \
                          "INNER JOIN users AS users_mentioning ON users_mentioning.id = tweets.userid " \
                          "WHERE users.followersnumber > 1000000 and users.screenname='BorisJohnson' OR users.screenname='Nigel_Farage' OR users.screenname = 'BBCNews' " \
                          "GROUP BY mentions.userid, users.screenname, users.followersnumber, users.friendsnumber, users_mentioning.id, tweets.userid, users_mentioning.screenname, users_mentioning.followersnumber, users_mentioning.friendsnumber " \
                          "ORDER BY tweet_counts DESC " \
                          "LIMIT 100;"
    User = namedtuple("User", 'id name followers_number friends_number')
    nodes, edges = set(), []
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    for i in cursor.fetchall():
        User(i[1], i[2], i[3], i[4])
        nodes.add(User(i[1], i[2], i[3], i[4]))
        nodes.add(User(i[5], i[6], i[7], i[8]))
        edges.append((i[1], i[5], i[0]))

    nodes_str, edges_str, attributes = create_input(list(nodes), edges, User)

    fill_gephi_file("gephi_raw_file.gexf", "gephi_mentions.gexf",
                    nodes_str, edges_str, attributes)


def hashtags(connection):
    SQL_QUERY = "SELECT count(hashtagid) AS hashtag_count, hashtags.id, hashtags.name, users.id, users.screenname, users.followersnumber, users.friendsnumber FROM TWEETSHASHTAGS " \
                "INNER JOIN tweets ON tweetid=tweets.id " \
                "INNER JOIN users ON users.id=tweets.userid " \
                "INNER JOIN hashtags ON hashtags.id=hashtagid " \
                "WHERE users.followersnumber > 1000000 " \
                "GROUP BY hashtags.id, hashtags.name, users.screenname, users.id, users.followersnumber, users.friendsnumber;" \

    User = namedtuple("User", 'id name followers_number friends_number')
    Hashtag = namedtuple("Hashtag", 'id name')
    nodes, edges = set(), []
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    for i in cursor.fetchall():
        nodes.add(User(i[3], i[4], i[5], i[6]))
        nodes.add(Hashtag(i[1], i[2]))
        edges.append((i[3], i[1], i[0]))

    nodes_str, edges_str, attributes = create_input(list(nodes), edges, User)

    fill_gephi_file("gephi_raw_file.gexf", "gephi_hashtags.gexf",
                    nodes_str, edges_str, attributes)


def user_sentiment(connection):
    SQL_QUERY = "SELECT users.id, users.screenname, avg(sentiment) AS sentiment_average, users.followersnumber FROM USERS "\
                 "INNER JOIN tweets on users.id = tweets.userid " \
                 "WHERE users.followersnumber > 100000 " \
                 "GROUP BY users.id, users.screenname, users.followersnumber " \
                 "ORDER BY users.followersnumber DESC " \
                 "LIMIT 100;"

    User = namedtuple("User", 'id name followers_number sentiment_average')
    nodes, edges = set(), []
    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    for i in cursor.fetchall():
        nodes.add(User(i[0], i[1], i[3], i[2]))

    nodes_str, edges_str, attributes = create_input_sentiment(list(nodes), edges, User)

    fill_gephi_file("gephi_raw_file.gexf", "gephi_sentiment.gexf",
                    nodes_str, edges_str, attributes)


def main():
    connection = connect_to_database()
    mentions(connection)
    retweets(connection)
    hashtags(connection)
    user_sentiment(connection)


if __name__ == "__main__":
    main()
