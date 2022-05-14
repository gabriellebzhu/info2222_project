'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''


from gevent import monkey; monkey.patch_all()
import bottle
from bottle import route, get, post, error, request, response, static_file, template
import model
import sec_helper as sec
from datetime import datetime
import json

app = bottle.Bottle()


@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------


# Allow image loading
@app.route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

# -----------------------------------------------------------------------------


# Allow CSS
@app.route('/css/<css:path>', name='static')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css')

#-----------------------------------------------------------------------------


# Allow javascript
@app.route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------


# Redirect to login
@app.get('/')
@app.get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

# -----------------------------------------------------------------------------


# Redirect to accounts/profile
@app.get('/profile')
def get_profile():
    '''
        get_index
        
        Serves the profile page
    '''
    return model.profile()

# -----------------------------------------------------------------------------


# Display the login page
@app.get('/login')
def get_login_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.login_form()


# Display the register page
@app.get('/join')
def get_register_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.register_form()


# Display the logout page
@app.route('/logout', methods=['POST', 'GET'])
def get_logout_controller():
    '''
        get_logout

        Serves the login page
    '''
    response.delete_cookie("account", secret=sec.COOKIE_SECRET)
    return model.logout()


# -----------------------------------------------------------------------------


# Attempt the login
@app.post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''
    # Handle the form processing
    username = request.json.get('username')
    password = request.json.get('password')
    user_pk = "null"
    # print(username)
    # print(password)
    # print(user_pk)
    
    # Call the appropriate method
    check = model.login_check(username, password, user_pk)

    if check[0]:
        response.set_cookie("account", username, secret=sec.COOKIE_SECRET)
        responding_msg = {'message': 'successful login', 'success': '1', 'isAdmin':check[1]}
    else:
        responding_msg = {'message': 'bad login', 'success': '0', 'isAdmin':check[1]}

    return responding_msg


# @post('/get_user_pk_json')
# def get_post_json():
#     data = request.get_json()
#     print("\n\n\n-------------------\n" + data)
#     response.content_type = 'application/json'

#     return data

@app.route('/_get_user_pk_json', methods=['POST', 'GET'])
def test():
    output = request.get_json()

    result = json.loads(output)  # this converts the json output to a python dictionary
    return result


# Attempt the register
@app.post('/register')
def post_register():
    '''
        post_register
        
        Handles register attempts
        Expects a form containing 'username' and 'password' fields
    '''
    # Handle the form processing
    username = request.json.get('username')
    password = request.json.get('password')
    user_pk = request.json.get('user_pk')
    print(username)
    print(password)
    print(user_pk)
    
    # Call the appropriate method
    check = model.register_new_user(username, password, user_pk)

    if check[0]:
        responding_msg = {'message': 'successful register', 'success': '1'}
    else:
        responding_msg = {'message': 'bad register', 'success': '0'}

    return responding_msg


# -----------------------------------------------------------------------------


@app.get('/about')
def get_about():
    '''
        get_about

        Serves the about page
    '''
    return model.about()


# -----------------------------------------------------------------------------


@app.route('/friends')
def get_friends():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.friend_list(username)


@app.post('/friends')
def add_friend():
    add_type = request.forms.get("add-type")

    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    if add_type == "add-username":
        friend_username = request.forms.get('username-input')
        return model.add_friend(username, friend_username)
    else:
        return model.add_random_friend(username)


@app.get('/chat/<friend_id:path>')
def get_chat_with_friend(friend_id):
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.friend_chat(username, friend_id)


@app.post('/chat/<friend_id:path>')
def send_msg(friend_id):
    message = request.json.get('message')
    secret = request.json.get('secret')
    model.save_secret(friend_id, secret)
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    model.save_msg(friend_id, username, message)
    return {'message': message, 'username': username}


# -----------------------------------------------------------------------------


@app.route('/manage')
def manage_classes():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.manage_form(username)


@app.post('/manage')
def manage_action():
    manage_type = request.forms.get("manage-type")
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)

    if manage_type == "add-class":
        class_code = request.forms.get('class-code-input')
        class_name = request.forms.get('class-name-input')
        return model.add_class(class_code, class_name, username)
    elif manage_type == "del-class":
        class_info = request.forms.get('class-info-input')
        return model.del_class(class_info, username)


@app.route('/manage/<class_code:path>')
def manage_classes(class_code):
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.manage_class_view(username, class_code)


@app.post('/manage/<class_code:path>')
def manage_classes(class_code):
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    manage_type = request.forms.get("manage-type")

    if manage_type == 'ban-student':
        to_ban = request.forms.getall("ban-students")
        return model.manage_class_ban(username, class_code, to_ban)
    elif manage_type == 'mute-student':
        to_mute = request.forms.getall("mute-students")
        return model.manage_class_mute(username, class_code, to_mute)
    elif manage_type == 'unban-student':
        to_ban = request.forms.getall("unban-students")
        return model.manage_class_unban(username, class_code, to_ban)
    elif manage_type == 'mute-student':
        to_mute = request.forms.getall("unmute-students")
        return model.manage_class_unmute(username, class_code, to_mute)


@app.route('/home')
def home():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.home(username)


# -----------------------------------------------------------------------------


@app.route('/posts')
def show_posts():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.show_posts(username)


@app.post('/posts')
def post_action():
    post_type = request.forms.get("post-type")
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)

    if post_type == "join-class":
        class_info = request.forms.get('class-info-input')
        return model.join_class(class_info, username)
    # elif post_type == "del-class":
    #     class_info = request.forms.get('class-info-input')
    #     return model.del_class(class_info, username)


@app.post("/posts/show")
def filter_posts():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    classes = request.forms.getall('class-choice')
    author_types = request.forms.getall('filter-choice')
    tags = request.forms.getall('tag-choice')
    tags += request.forms.get('tag-search').split()
    search_term = request.forms.get('search')
    return model.show_filtered(username, classes, author_types, tags, search_term)


@app.route('/posts/new')
def new_post():
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    return model.new_post_form(username)


@app.post('/posts/new')
def add_post():
    post_title = request.forms.get("post-title")
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    class_code = request.forms.get("post-class-selector")
    tags = request.forms.get("post-tags")
    body = request.forms.get("post-body")
    uploads = request.files.getall("post-attachments")

    return model.create_post(post_title, username, today,
                             class_code, tags, body, uploads)


@app.route('/posts/<post_id:int>')
def new_post(post_id):
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)

    return model.view_post(username, post_id)


@app.route('/uploads/<source:path>')
def new_post(source=None):
    if source is not None:
        return model.view_source(source)



# 
# -----------------------------------------------------------------------------


# Help with debugging
@app.post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@app.error(404)
def error(error):
    return model.handle_errors(error)
