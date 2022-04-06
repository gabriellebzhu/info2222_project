import sqlite3
import os

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
            print(sql_string)
            out = self.cur.execute(string)
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

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

        # Add our admin user
        self.add_user('admin', admin_password, salt=os.urandom(16), public_key="test_key", admin=1)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, salt, public_key, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES(NULL, "{username}", "{password}", "{salt}", "{pk}", {admin})
            """

        sql_cmd = sql_cmd.format(username=username, password=password, salt=salt, admin=admin,
                                 pk=public_key)

        print(self.execute(sql_cmd))
        self.commit()
        return True

    #-----------------------------------------------------------------------------

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
            return True
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

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False


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
