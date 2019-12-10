import psycopg2
from collections import defaultdict
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


def create_mentions_input(connection, nodes, edges):
    nodes_string_list = []
    edges_string_list = []
    attributes_definiton = [ATTIBUTE_DEFINE_BASE_ROW % ('location', 'Location', 'string'),
                            ATTIBUTE_DEFINE_BASE_ROW % ('followers_number', 'Followers number', 'int'),
                            ATTIBUTE_DEFINE_BASE_ROW % ('friends_number', 'Friends number', 'int')]

    cursor = connection.cursor()
    for i, edge in enumerate(edges.items()):
        user_mention_id, user_mentioned_id = edge[0]
        mentions_number = edge[1]
        if user_mention_id in nodes and user_mentioned_id in nodes:
            edges_string_list.append(EDGE_BASE_ROW % (i, user_mention_id, user_mentioned_id, mentions_number))

    for node_id in nodes:
        cursor.execute("SELECT name, location, followersnumber, friendsnumber from USERS WHERE id = %s", (node_id,))
        record = cursor.fetchone()
        if record:
            user_name = record[0]
            location = record[1]
            followers_number = record[2]
            friends_number = record[3]
            attributes = [ATTVALUE_BASE_ROW % ('location', location),
                          ATTVALUE_BASE_ROW % ('followers_number', followers_number),
                          ATTVALUE_BASE_ROW % ('friends_number', friends_number)]

            node = NODE_ATTRIBUTE_BASE_ROW % (node_id, user_name, ("\n".join(attributes)))
            nodes_string_list.append(node)

    return nodes_string_list, edges_string_list, "\n".join(attributes_definiton)


def get_mentions_data(connection, user_mentions):
    mentions = defaultdict(lambda: [])
    edges = defaultdict(lambda: 1)
    nodes = set()

    # user_mentions = cursor
    for record in user_mentions:
        tweet_id = record[0]
        user_mention_id = record[1]
        cursor2 = connection.cursor()
        cursor2.execute("SELECT userId FROM Tweets WHERE id = %s", (tweet_id, ))
        user_mentioned_id = cursor2.fetchone()[0]
        mentions[user_mention_id].append(user_mentioned_id)
        nodes.add(user_mention_id)
        nodes.add(user_mentioned_id)

    for entry in mentions.items():
        user_mention = entry[0]
        users_mentioned = entry[1]
        for user_mentioned in users_mentioned:
            edges[(user_mention, user_mentioned)] += 1

    return edges, nodes


def create_mentions_file(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Mentions;")
    user_mentions = cursor.fetchmany(100)
    edges, nodes = get_mentions_data(connection, user_mentions)
    nodes_string_list, edges_string_list, attributes = create_mentions_input(connection, nodes, edges)
    fill_gephi_file("gephi_raw_file.gexf",
                    "/home/justyna/Studies/2. semestr/ED/gephi/gephi_mentions-with attributes18.gexf",
                    nodes_string_list, edges_string_list, attributes)


def get_retwets_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Retweets;")
    user_mentions = cursor.fetchmany(100)
    edges, nodes = get_mentions_data(connection, user_mentions)
    nodes_string_list, edges_string_list, attributes = create_mentions_input(connection, nodes, edges)
    fill_gephi_file("gephi_raw_file.gexf",
                    "/home/justyna/Studies/2. semestr/ED/gephi/gephi_retweets.gexf",
                    nodes_string_list, edges_string_list, attributes)


def main():
    connection = connect_to_database()
    get_retwets_data(connection)


if __name__ == "__main__":
    main()
