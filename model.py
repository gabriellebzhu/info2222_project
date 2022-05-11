'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import json
import view
import random
import sql

from bottle import request
import os

import sec_helper as sec

from Crypto.PublicKey import RSA

db = sql.SQLDatabase("test.db")
db.database_setup()


# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    # data = {"to_display":"HI, how are you"}
    return page_view("login", data=get_server_public_key(), is_admin=0)

def logout():
    return page_view("logout", ext=".tpl")


#-----------------------------------------------------------------------------

def register_form():
    return page_view("register")


# Check the login credentials
def login_check(username, password, pk):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    message = "The username or password you entered was incorrect"

    # By default assume good creds
    login = True

    if not db.check_user_exists(username=username):
        login = False
    else:
        salt = db.get_salt_from_username(username)
        hashed = sec.hash_the_pass(password, salt)
        if not db.check_credentials(username, hashed):
            login = False

    if login:
        is_admin = db.get_is_admin(username)
        return True, f"{is_admin}"
    else:
        return False, "False"


# Register User
def register_new_user(username, password, pk):
    global db
    # By default assume good creds
    register = True
    err_str = "Valid!"

    # if username is in database, error of "USER ALREADY EXISTS"
    user_exists = db.check_user_exists(username=username)
    if user_exists:
        register = False
        err_str = "Account already exists"
    elif not username:
        register = False
        err_str = "No username provided"
    elif not check_password_security(password, username):
        register = False
        err_str = "Password is very easy to guess."

    if register:
        salt = os.urandom(16)  # 16 bytes of random salt
        hashed = sec.hash_the_pass(password, salt)
        db.add_user(username=username, password=hashed, salt=salt,
                    public_key=pk, admin=0)
        return True, page_view("valid", name=username, is_register="true")
    else:
        return False, page_view("invalid", reason=err_str)


def check_password_security(password, username):
    if len(password) < 3:
        return False
    elif password == username:
        return False
    
    return True


# -----------------------------------------------------------------------------
# FRIENDS
# -----------------------------------------------------------------------------

def add_friend(username, friend_username):
    if username and friend_username:
        friend_ids, friends = db.get_one_way_friends(username)
        check = db.add_friend(username, friend_username)
        if check is True:
            return page_view("friends/populateFriends", ext=".tpl", username=username,
                             friend_usernames=friends, friend_ids=friend_ids,
                             add_msg="Successfully added!", err_msg="")
        elif check == -1:
            return page_view("friends/populateFriends", ext=".tpl", username=username,
                             friend_usernames=friends, friend_ids=friend_ids, err_msg="",
                             add_msg=f"You are already friends with {friend_username}")
        else:
            add_msg = "User not found."
            return page_view("friends/populateFriends", ext=".tpl", username=username,
                             friend_usernames=friends, friend_ids=friend_ids,
                             add_msg=add_msg, err_msg="")


def add_random_friend(username):
    if username:
        friend_ids, friends = db.get_one_way_friends(username)
        classes = db.get_classes(username)
        if not classes:
            add_msg = "You are not yet enrolled in any classes."
            return page_view("friends/populateFriends", ext=".tpl", username=username,
                             friend_usernames=friends, friend_ids=friend_ids,
                             add_msg=add_msg, err_msg="")

        while True:
            class_ind = random.randint(0, len(classes) - 1)
            random_usrname = db.get_random_user(username, classes[class_ind])
            if random_usrname:
                break

            classes.remove(classes[class_ind])
            if len(classes) < 1:
                add_msg = "No new friends to add from any of your classes."
                return page_view("friends/populateFriends", ext=".tpl", username=username,
                                 friend_usernames=friends, friend_ids=friend_ids,
                                 add_msg=add_msg, err_msg="")
        add_friend(username, random_usrname)


def friend_list(username):
    if username:
        friend_ids, friends = db.get_one_way_friends(username)
        return page_view("friends/populateFriends", ext=".tpl", username=username,
                         friend_usernames=friends, friend_ids=friend_ids,
                         add_msg="", err_msg="")
    else:
        return page_view("invalid", reason="Login before chatting with others!")


def friend_chat(username, friend_id):
    err_msg = "Error finding user at this link. Talk to someone else?"
    # check that username is indeed logged in
    if not username:
        return page_view("invalid", reason="Login before chatting with others!")

    # Check that the friend_id exists
    this_username, friend_username = db.get_users_from_friend_id(friend_id)

    if username == friend_username:
        friend_username = this_username
        this_username = username

    if this_username != username:
        return page_view("friends/populateFriends", ext=".tpl", username=username,
                         friend_usernames=[], friend_ids=[],
                         add_msg="", err_msg=err_msg)

    friend_ids, friends = db.get_one_way_friends(username)
    old_chat = db.get_recent_msgs(friend_id)
    old_chat2 = json.dumps(old_chat)
    friend_pk = db.get_friend_pk(friend_username)
    print(friend_pk)
    key_and_iv = db.get_secret(friend_id)
    return page_view("friends/chat", ext=".tpl", err_msg="",
                     friend_username=friend_username, friend_pk=friend_pk,
                     username=username, friend_id=friend_id,
                     friend_usernames=friends, friend_ids=friend_ids,
                     key_and_iv=key_and_iv, old_chat2=old_chat2)


def save_secret(friend_id, secret):
    if secret != 'None':
        db.add_secret(friend_id, secret)


def server_key_gen():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("key/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("key/public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

#-----------------------------------------------------------------------------
# Profile
#-----------------------------------------------------------------------------

def profile():
    '''
        profile
        Returns the view for the profile
    '''
    # if username:
    #     pass
    # else:
    #     return page_view("invalid", reason="Login before viewing profile!")

    return page_view("profile")

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------


def manage_form(username):
    if username and db.get_is_admin(username):
        classes = db.get_admin_classes(username)
        return page_view("admin/manage", ext=".tpl", username=username,
                         classes=classes,
                         msg="", err_msg="")
    elif username:
        return page_view("invalid", reason="You do not have access to this page.")
    else:
        return page_view("invalid", reason="Please log in before viewing this page.")


def add_class(class_code, class_name, admin_username):
    if admin_username and db.get_is_admin(admin_username):
        pass
    elif admin_username:
        return page_view("invalid", reason="You do not have access to this page.")
    else:
        return page_view("invalid", reason="Please log in before viewing this page.")

    classes = db.get_admin_classes(admin_username)

    if class_code:
        class_code = class_code.upper()
    else:
        return page_view("admin/manage", ext=".tpl", username=admin_username,
                         classes=classes,
                         msg="Please input a class code!", err_msg="")

    if class_name:
        class_name = class_name.title()
    else:
        return page_view("admin/manage", ext=".tpl", username=admin_username,
                         classes=classes,
                         msg="Please input a class name", err_msg="")

    check = db.add_class(class_code, class_name, admin_username)

    if check == 0:
        return page_view("admin/manage", ext=".tpl", username=admin_username,
                         classes=classes, msg="You are already managing this class", err_msg="")
    elif check == 2:
        classes = db.get_admin_classes(admin_username)
        msg = f"You have been added as an admin to {class_code}: {class_name}"
        return page_view("admin/manage", ext=".tpl", username=admin_username,
                         classes=classes, msg=msg, err_msg="")
    else:
        classes = db.get_admin_classes(admin_username)
        msg = f"You have created the class {class_code}: {class_name}."
        return page_view("admin/manage", ext=".tpl", username=admin_username,
                         classes=classes, msg=msg, err_msg="")


def del_class(class_info, username):
    if username and db.get_is_admin(username):
        pass
    elif username:
        return page_view("invalid", reason="You do not have access to this page.")
    else:
        return page_view("invalid", reason="Please log in before viewing this page.")

    classes = db.get_admin_classes(username)

    if not class_info:
        msg = "Please enter the class code or the class name of the class to be deleted"
        return page_view("admin/manage", ext=".tpl", username=username,
                         classes=classes, msg=msg, err_msg="")

    check, class_code, class_name = db.del_class(class_info, username)
    if check == 0:
        return page_view("admin/manage", ext=".tpl", username=username,
                         classes=classes, msg="No such class", err_msg="")
    elif check == 1:
        classes = db.get_admin_classes(username)
        msg = f"You deleted {class_code}: {class_name}"
        return page_view("admin/manage", ext=".tpl", username=username,
                         classes=classes, msg=msg, err_msg="")
    else:
        classes = db.get_admin_classes(username)
        msg = f"You must be an administrator of {class_code}: {class_name} to delete it."
        return page_view("admin/manage", ext=".tpl", username=username,
                         classes=classes, msg=msg, err_msg="")


# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------


def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())


# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)


def get_server_public_key():
    key = "none"
    with open('key/server_public.pem', 'r') as f:
        key = f.read()
        key = key.split('\n')
        key = '\\\n'.join(key)

    return key

def save_msg(friend_id, username, message):
    db.add_message(friend_id, username, message)
    db.get_recent_msgs(friend_id)