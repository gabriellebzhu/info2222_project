import sqlite3
import os

import sec_helper as sec

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

# END TO END ENCRYPTION
# 1. alice and bob register themselves in the system
# 2. after registration, they generate their public key pair in their browser (frontend), and send their public key to the server (stored in the user table)
# 3. alice want start communicating with bob, needs to create a session key with bob if there is not one. session key used to symmetrically encrypt the actual message. for this session key, it needs to be encrypted with bob's public key. NEED TO ATTACH SIGNATURE USING ALICES PRIVATE KEY
# 4. bob decrypt the session key with bob private key. bob will decrypt the actual message with the session key. Check that the signature is ok with alice's public key.

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            out = self.cur.execute(string)
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):
        # # Clear the database if needed
        # self.execute("DROP TABLE IF EXISTS Users")
        # self.commit()

        self.cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Users';""")
        if self.cur.fetchone()[0] == 0:
            # Create the users table
            self.execute("""CREATE TABLE Users(
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                salt TEXT,
                pk TEXT,
                admin INTEGER DEFAULT 0
            )""")

            self.commit()
        
        self.cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Friends';""")
        if self.cur.fetchone()[0] == 0:
            # Create the users table
            self.execute("""CREATE TABLE Friends(
                friend_id INTEGER PRIMARY KEY,
                user_id1 INTEGER,
                user_id2 INTEGER
            )""")

            self.commit()

        salt = os.urandom(16)
        hashed = sec.hash_the_pass(admin_password, salt)

        # Add our admin user
        self.add_user('admin', hashed, salt=salt, public_key="test_key", admin=1)

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, salt, public_key, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES(NULL, "{username}", "{password}", "{salt}", "{pk}", {admin})
            """
        salt = sec.salt_to_string(salt)
        sql_cmd = sql_cmd.format(username=username, password=password, salt=salt, admin=admin,
                                 pk=public_key)

        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)

        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    def get_hashpass_from_username(self, username):
        sql_query = """
                SELECT password
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return self.cur.fetchone()[0]
        else:
            return False

    def get_salt_from_username(self, username):
        sql_query = """
                SELECT salt
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        self.execute(sql_query)

        salt = self.cur.fetchone()[0]
        salt = sec.string_to_salt(salt)
        return salt

    def check_user_exists(self, username):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    # -----------------------------------------------------------------------------
    # Friend Handling
    # -----------------------------------------------------------------------------

    def add_friend(self, username, friend_username):
        user_id_1_cmd = f"SELECT id FROM Users WHERE username = '{username}'"
        user_id_2_cmd = f"SELECT id FROM Users WHERE username = '{friend_username}'"

        self.execute(user_id_1_cmd)
        if not self.cur.fetchone():
            return False
        user_id1 = self.cur.fetchone()[0]

        self.execute(user_id_2_cmd)
        if not self.cur.fetchone():
            return False
        user_id2 = self.cur.fetchone()[0]

        insert_friends = f"INSERT INTO Friends VALUES(NULL, '{user_id1}', '{user_id2}');"

        self.execute(insert_friends)
        self.commit()
        return True

    def get_one_way_friends(self, username):
        """
            Get the usernames of all of username's friends (who may or may not consider
            username a friend as well).

            :return: list of friends' usernames as strings
        """
        friend_ids_cmd = """SELECT F.Username AS FriendUsername
                            FROM Users AS U
                            JOIN Friends AS UtoF ON UtoF.user_id1 = U.ID
                            JOIN Users AS F ON F.id = UtoF.user_id2
                            where U.username = '{username}' """

        friend_ids_cmd = friend_ids_cmd.format(username=username)

        self.execute(friend_ids_cmd)
        friends = [friend[0] for friend in self.cur.fetchall()]
        if not friends:
            return None

        return friends

    def get_mutual_friends(self, username):
        """
            Get the usernames of all of username's friends who do consider
            username a friend as well. (IN PROGRESS)
        """
        friend_ids_cmd = """SELECT U.id UserID, U.username AS Username, F.Username AS FriendUsername
                            FROM Users AS U
                            JOIN Friends AS UtoF ON UtoF.user_id1 = U.id
                            JOIN Users AS F ON F.id = UtoF.user_id2
                            WHERE U.username = "{username}";
                            """

        friend_ids_cmd = friend_ids_cmd.format(username=username)

        self.execute(friend_ids_cmd)
        if not self.cur.fetchall():
            return None

        return self.cur.fetchall()

    def peek(self):
        sql_query = """
                SELECT username
                FROM Users
            """

        sql_query = sql_query.format()

        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False
