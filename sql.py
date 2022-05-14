import random
import sqlite3
import os
import re

import sec_helper as sec

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models



class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()
        self.conn.create_function("REGEXP", 2, SQLDatabase.regexp)

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

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # Setup 
    # -----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):
        # # Clear the database if needed
        # self.execute("DROP TABLE IF EXISTS Users")
        # self.commit()

        user_cols = """id INTEGER PRIMARY KEY, username TEXT, password TEXT,
                       salt TEXT, pk TEXT, admin INTEGER DEFAULT 0"""
        self.create_table("Users", user_cols)

        admin_cols = """username TEXT, admin_type TEXT"""
        self.create_table("Admins", admin_cols)

        friends_cols = """friend_id TEXT, user_id1 INTEGER, user_id2 INTEGER"""
        self.create_table("Friends", friends_cols)

        chats_cols = """msg_id INTEGER PRIMARY KEY, friend_id TEXT, sender_username TEXT, message TEXT"""
        self.create_table("Chats", chats_cols)

        secrets_cols = """friend_id TEXT, key_and_iv TEXT"""
        self.create_table("Secrets", secrets_cols)

        classes_cols = """class_id INTEGER PRIMARY KEY, class_name TEXT, class_code TEXT, admin_user_id INTEGER"""
        self.create_table("Classes", classes_cols)

        enrolled_cols = """class_code TEXT, student_username TEXT, visible INTEGER"""
        self.create_table("Enrollments", enrolled_cols)

        post_cols = """post_id INTEGER PRIMARY KEY, title TEXT, author_username TEXT, date TEXT, class_code TEXT, tags TEXT, body TEXT, upload TEXT, likes INTEGER"""
        self.create_table("Posts", post_cols)

        tag_col = """tag TEXT, freq INTEGER"""
        self.create_table("Tags", tag_col)

        liked_col = """post_id INTEGER, username TEXT"""
        self.create_table("Liked", liked_col)

        muted = """class_code TEXT, student_username TEXT"""
        self.create_table("Muted", muted)

        banned = """class_code TEXT, student_username TEXT"""
        self.create_table("Banned", banned)

        profile_col = """username TEXT, year TEXT, hometown TEXT, majors TEXT, public INTEGER"""
        self.create_table("Profiles", profile_col)


    def create_table(self, name, columns):
        self.cur.execute("""SELECT count(name)
                            FROM sqlite_master WHERE type='table'
                            AND name='{name}';""".format(name=name))
        if self.cur.fetchone()[0] == 0:
            # Create the users table
            self.execute("""CREATE TABLE {name}(
                {columns}
            )""".format(name=name, columns=columns))

            self.commit()

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

    # update pk
    def user_pk_update(self, username, new_public_key):
        sql_cmd = """
                UPDATE Users
                SET pk = '{pk}'
                WHERE username = '{username}'
            """
        sql_cmd = sql_cmd.format(username=username,
                                 pk=new_public_key)

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

    def get_is_admin(self, username):
        sql_query = """
                SELECT 1
                FROM Admins
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        print(username)
        self.execute(sql_query)

        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    # -----------------------------------------------------------------------------
    # Classes 
    # -----------------------------------------------------------------------------

    def add_class(self, class_code, class_name, admin):
        sql_cmd = """
                INSERT INTO Classes
                VALUES(NULL, "{class_name}", "{class_code}", {admin_id})
            """

        admin_id_cmd = f"SELECT id From Users Where username='{admin}'"
        self.execute(admin_id_cmd)
        admin_id = self.cur.fetchone()[0]

        exists_cmd = f"SELECT 1 From Classes WHERE admin_user_id='{admin_id}' AND class_code='{class_code}'"
        self.execute(exists_cmd)
        if self.cur.fetchone():
            return 0

        add_admin_cmd = f"SELECT 1 From Classes WHERE class_code='{class_code}'"
        self.execute(add_admin_cmd)
        not_original = self.cur.fetchone()

        sql_cmd = sql_cmd.format(class_name=class_name, class_code=class_code,
                                 admin_id=admin_id)

        self.execute(sql_cmd)
        self.commit()

        if not_original:
            # Current user was not the original admin, but now has become one.
            return 2
        return 1

    def del_class(self, class_info, username):
        sql_cmd = ""
        del_type = 0
        class_name = ""
        class_code = ""

        is_code_cmd = f"SELECT Classes.class_name, Users.username FROM Classes INNER JOIN Users ON Classes.admin_user_id = Users.id WHERE Classes.class_code='{class_info.upper()}'"

        self.execute(is_code_cmd)
        info = self.cur.fetchall()
        if info:
            admins = [item[1] for item in info]
            authorised = username in admins

            if authorised:
                sql_cmd = f"DELETE FROM Classes WHERE class_code='{class_info}'"
                del_type = 1
            else:
                del_type = -1

            class_code = class_info
            class_name = info[0][0]

        is_name_cmd = f"SELECT Classes.class_code, Users.username FROM Classes INNER JOIN Users ON Classes.admin_user_id = Users.id WHERE Classes.class_name='{class_info.title()}'"

        self.execute(is_name_cmd)
        info = self.cur.fetchall()
        if info:
            admins = [item[1] for item in info]
            authorised = username in admins

            if authorised:
                sql_cmd = f"DELETE FROM Classes WHERE class_name='{class_info}'"
                del_type = 1
            else:
                del_type = -1

            class_name = class_info
            class_code = info[0][0]

        if not sql_cmd:
            return del_type, "", ""

        self.execute(sql_cmd)
        self.commit()

        return del_type, class_code, class_name

    def join_class(self, class_info, username):
        result_type = 0
        class_name = ""
        class_code = ""

        is_code_cmd = f"SELECT class_name FROM Classes WHERE class_code='{class_info.upper()}'"
        self.execute(is_code_cmd)
        info = self.cur.fetchone()
        if info:
            result_type = 1
            class_code = class_info.upper()
            class_name = info[0].title()

        is_name_cmd = f"SELECT class_code FROM Classes WHERE class_name='{class_info.title()}'"
        self.execute(is_name_cmd)
        info = self.cur.fetchone()
        if info:
            result_type = 1
            class_name = class_info.title()
            class_code = info[0].upper()

        if not result_type:
            return result_type, class_code, class_name

        if username in self.get_banned(class_code):
            return -2, class_code, class_name

        reenroll = f"SELECT 1 FROM Enrollments WHERE student_username='{username}' AND class_code='{class_code}'"

        self.execute(reenroll)
        if self.cur.fetchone():
            return -1, class_code.upper(), class_name.title()  # user is already enrolled

        enroll = f"INSERT INTO Enrollments VALUES('{class_code.upper()}', '{username}', 1)"
        self.execute(enroll)
        self.commit()

        return result_type, class_code.upper(), class_name.title()



    def get_classes(self, username):
        sql_query = """
                SELECT class_code
                FROM Enrollments
                WHERE student_username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        self.execute(sql_query)

        classes = [class_code[0] for class_code in self.cur.fetchall()]
        return classes

    def get_admin_classes(self, admin):
        sql_query = """
                SELECT Classes.class_code
                FROM Classes
                INNER JOIN Users ON Classes.admin_user_id = Users.id
                WHERE Users.username = '{admin}'
            """

        sql_query = sql_query.format(admin=admin)

        self.execute(sql_query)

        classes = [class_code[0] for class_code in self.cur.fetchall()]
        return classes

    def get_random_user(self, username, class_code):
        sql_query = """
                SELECT student_username
                    FROM Enrollments
                    WHERE class_code = '{class_code}'
                    AND visible=1
                    AND student_username != '{username}'

                EXCEPT

                SELECT * FROM (
                    SELECT u1.username from Friends 
                        INNER JOIN Users as u1 ON Friends.user_id1 = u1.id 
                        INNER JOIN Users as u2 ON Friends.user_id2 = u2.id 
                        WHERE u2.username = '{username}'
                    UNION
                    SELECT u2.username from Friends 
                        INNER JOIN Users as u1 ON Friends.user_id1 = u1.id 
                        INNER JOIN Users as u2 ON Friends.user_id2 = u2.id 
                        WHERE u1.username = '{username}'
                )

            """

        sql_query = sql_query.format(class_code=class_code, username=username)

        self.execute(sql_query)
        students = [student[0] for student in self.cur.fetchall()]
        print(f"from {class_code}, get {students}")
        if len(students) < 1:
            return None
        student_index = random.randint(0, len(students) - 1)

        return students[student_index]

    def get_students(self, class_code):
        cmd = f"Select student_username FROM Enrollments WHERE class_code='{class_code}'"

        self.execute(cmd)
        return [item[0] for item in self.cur.fetchall()]

    def get_banned(self, class_code):
        cmd = f"Select student_username FROM Banned WHERE class_code='{class_code}'"

        self.execute(cmd)
        return [item[0] for item in self.cur.fetchall()]

    def get_muted(self, class_code):
        cmd = f"Select student_username FROM Muted WHERE class_code='{class_code}'"

        self.execute(cmd)
        return [item[0] for item in self.cur.fetchall()]
    
    def get_muted_classes(self, username):
        cmd = f"Select class_code FROM Muted WHERE student_username='{username}'"

        self.execute(cmd)
        return [item[0] for item in self.cur.fetchall()]

    def ban(self, class_code, students):
        for student in students:
            cmd = f"Insert into Banned Values('{class_code}', '{student}')"
            self.execute(cmd)
            self.commit()

            cmd = f"Delete from Enrollments Where class_code='{class_code}' and student_username='{student}'"
            self.execute(cmd)
            self.commit()

    def unban(self, class_code, students):
        for student in students:
            cmd = f"Delete from Banned Where class_code='{class_code}' and student_username='{student}'"
            self.execute(cmd)
            self.commit()

    def mute(self, class_code, students):
        for student in students:
            cmd = f"Insert into Muted Values('{class_code}', '{student}')"
            self.execute(cmd)
            self.commit()

    def unmute(self, class_code, students):
        for student in students:
            cmd = f"delete from Muted where class_code='{class_code}' and student_username='{student}')"
            self.execute(cmd)
            self.commit()


    # -----------------------------------------------------------------------------
    # Posts
    # -----------------------------------------------------------------------------

    def add_post(self, title, username, date,
                 class_code, tags, body, upload_paths):
        tags = self.tag(tags)
        enroll = f"INSERT INTO Posts VALUES(NULL, '{title}', '{username}', '{date}', '{class_code}', '{tags}', '{body}', '{upload_paths}', 0)"
        self.execute(enroll)
        self.commit()
        return self.cur.lastrowid

    def tag(self, tags):
        tags = list(set(tags.split()))
        for tag in tags:
            exists_cmd = f"SELECT 1 from Tags Where tag='{tag}'"
            self.execute(exists_cmd)
            if self.cur.fetchone():
                cmd = f"UPDATE Tags SET freq = freq + 1 WHERE tag='{tag}'"
            else:
                cmd = f"INSERT into Tags VALUES('{tag}', 1)"
            
            self.execute(cmd)
            self.commit()
        return ' '.join(tags)

    def five_popular_tags(self):
        cmd = "SELECT tag FROM Tags ORDER BY freq DESC, tag ASC LIMIT 5"

        self.execute(cmd)
        data = [item[0] for item in self.cur.fetchall()]
        return data

    def get_post_from_id(self, username, post_id):
        get_post = f"SELECT * FROM Posts WHERE post_id='{post_id}'"

        self.execute(get_post)
        data = self.cur.fetchone()
        if not data:
            return 0, None
        elif data[2] == username:
            return 2, data
        else:
            return 1, data

    def get_admins(self):
        cmd = "SELECT username from Admins"
        self.execute(cmd)
        return [item[0] for item in self.cur.fetchall()]

    def filter(self, username, classes, author_types, tags, search_term):
        if not classes:
            classes = self.get_classes(username)

        if not author_types or len(author_types) == 2:
            author_cmd = ""
        else:
            admins = ','.join([f"'{admin}'" for admin in self.get_admins()])
            if "1" in author_types:
                author_cmd = f"AND author_username IN ({admins})"
            else:
                author_cmd = f"AND author_username NOT IN ({admins})"

        if not search_term:
            search_term = ".*"

        classes = ','.join([f"'{class_code}'" for class_code in classes])
        print(classes, author_cmd)

        cmd = """SELECT * FROM Posts
                    WHERE (title REGEXP '{search_term}'
                    OR author_username REGEXP '{search_term}'
                    OR body REGEXP '{search_term}')
                    AND
                    (class_code IN ({classes}))
                {author_cmd}
                """
        cmd = cmd.format(search_term=search_term, author_cmd=author_cmd, classes=classes)

        self.execute(cmd)
        data = self.cur.fetchall()

        if tags:
            filtered = []
            for entry in data:
                tag_data = entry[5].split()
                for tag in tags:
                    if tag in tag_data:
                        filtered.append(entry)
                        break
            return filtered
        else:
            return data

    def regexp(expr, item):
        reg = re.compile(expr)
        return reg.search(item) is not None

    # -----------------------------------------------------------------------------
    # Friend Handling
    # -----------------------------------------------------------------------------

    def add_friend(self, username, friend_username):
        user_id_1_cmd = f"SELECT id FROM Users WHERE username = '{username}'"
        user_id_2_cmd = f"SELECT id FROM Users WHERE username = '{friend_username}'"

        self.execute(user_id_1_cmd)
        result = self.cur.fetchone()
        if not result:
            return 0
        user_id1 = result[0]

        self.execute(user_id_2_cmd)
        result = self.cur.fetchone()
        if not result:
            return 0
        user_id2 = result[0]

        exist_cmd = f"SELECT 1 FROM Friends WHERE user_id1='{user_id1}' AND user_id2 = '{user_id2}'"
        self.execute(exist_cmd)
        result = self.cur.fetchone()
        if result:
            return -1

        # allocate random friend id for friend pair
        while True:
            friend_id = sec.salt_to_string(os.urandom(16))
            check_id_uniq_sql = f"SELECT 1 from Friends where friend_id = '{friend_id}'"
            self.execute(check_id_uniq_sql)

            if not self.cur.fetchone():
                break

        insert_friends = f"INSERT INTO Friends VALUES('{friend_id}', '{user_id1}', '{user_id2}');"

        self.execute(insert_friends)
        self.commit()
        return True

    def get_friend_pk(self, friend_username):
        pk_cmd = f"select pk from Users where username='{friend_username}'"
        self.execute(pk_cmd)
        pk = self.cur.fetchone()[0]
        pk = '\\r\\n'.join(pk.split("\r\n"))
        return pk

    def get_one_way_friends(self, username):
        """
            Get the usernames of all of username's friends (who may or may not consider
            username a friend as well).

            :return: list of friends' usernames as strings
        """
        friend_ids_cmd = """SELECT UtoF.friend_id AS FriendID, F.Username AS FriendUsername
                            FROM Users AS U
                            JOIN Friends AS UtoF ON UtoF.user_id1 = U.ID
                            JOIN Users AS F ON F.id = UtoF.user_id2
                            where U.username = '{username}' """

        friend_ids_cmd = friend_ids_cmd.format(username=username)

        self.execute(friend_ids_cmd)
        friend_ls = self.cur.fetchall()
        
        friend_ids_cmd = """SELECT UtoF.friend_id AS FriendID, F.Username AS FriendUsername
                            FROM Users AS U
                            JOIN Friends AS UtoF ON UtoF.user_id2 = U.ID
                            JOIN Users AS F ON F.id = UtoF.user_id1
                            where U.username = '{username}' """.format(username=username)

        self.execute(friend_ids_cmd)
        friend_ls += self.cur.fetchall()
        print("1-way:", friend_ls)
        if not friend_ls:
            return ([], [])
        friend_id = [friend[0] for friend in friend_ls]
        friends = [friend[1] for friend in friend_ls]

        return friend_id, friends

    def get_users_from_friend_id(self, friend_id):
        friend_usrname_sql = """SELECT U.username AS Username, F.username AS FriendUsername
                    FROM Users AS U
                    JOIN Friends AS UtoF ON UtoF.user_id1 = U.id
                    JOIN Users AS F ON F.id = UtoF.user_id2
                    where UtoF.friend_id = '{friend_id}' """
        friend_usrname_sql = friend_usrname_sql.format(friend_id=friend_id)
        
        self.execute(friend_usrname_sql)
        result = self.cur.fetchone()
        if not result:
            return False
        return result


    # -----------------------------------------------------------------------------
    # Chat Backlog
    # -----------------------------------------------------------------------------

    def add_message(self, friend_id, sender_username, message):
        insert_message = f"INSERT INTO Chats VALUES(NULL, '{friend_id}', \
                           '{sender_username}', '{message}');"
        self.execute(insert_message)
        self.commit()

    def get_recent_msgs(self, friend_id):
        retrieve = """SELECT sender_username, message FROM (
                        SELECT * FROM Chats
                        WHERE friend_id = '{friend_id}'
                        ORDER BY msg_id DESC LIMIT 10
                      ) sub
                      ORDER BY msg_id ASC""".format(friend_id=friend_id)
        self.execute(retrieve)

        result = self.cur.fetchall()
        return result

    def add_secret(self, friend_id, key_and_iv):
        insert_key = f"INSERT INTO Secrets VALUES('{friend_id}', '{key_and_iv}');"
        self.execute(insert_key)
        self.commit()

    def get_secret(self, friend_id):
        retrieve = """SELECT key_and_iv
                      FROM Secrets
                      WHERE friend_id='{friend_id}'""".format(friend_id=friend_id)
        self.execute(retrieve)

        result = self.cur.fetchone()
        if not result:
            return "None"
        else:
            return result[0]

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

