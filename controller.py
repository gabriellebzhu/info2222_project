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


# Display the login page
@app.get('/login')
def get_login_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.login_form()


# Display the login page
@app.get('/register')
def get_register_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.register_form()


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
        responding_msg = {'message': 'successful login', 'success': '1'}
    else:
        responding_msg = {'message': 'bad login', 'success': '0'}

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


# Help with debugging
@app.post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------


# 404 errors, use the same trick for other types of errors
@app.error(404)
def error(error):
    return model.handle_errors(error)



# TESTINNG SMT OUT!!

# import uuid
# import inspect

# from gevent import monkey; monkey.patch_all()
# from gevent.event import Event
# from beaker.middleware import SessionMiddleware

# cache_size = 200
# cache = []
# new_message_event = Event()

# class BeakerPlugin(object):
#     name = 'beaker'

#     def setup(self, app):
#         ''' Make sure that other installed plugins don't affect the same
#             keyword argument.'''
#         for other in app.plugins:
#             if not isinstance(other, BeakerPlugin): continue
#             if other.keyword == self.keyword:
#                 raise PluginError("Found another beaker session plugin "\
#                     "with conflicting settings (non-unique keyword).")

#     def apply(self, callback, context):
#         args = inspect.getargspec(context['callback'])[0]
#         keyword = 'session'
#         if keyword not in args:
#             return callback
#         def wrapper(*a, **ka):
#             session = request.environ.get('beaker.session')
#             ka[keyword] = session
#             rv = callback(*a, **ka)
#             session.save()
#             return rv
#         return wrapper


# @route("/", template='index')
# def main(session):
#     global cache
#     if cache:
#         session['cursor'] = cache[-1]['id']
#     return {'messages': cache}

# @app.route('/a/message/new', method='POST')
# def message_new():
#     global cache
#     global cache_size
#     global new_message_event
#     name = request.environ.get('REMOTE_ADDR') or 'Anonymous'
#     forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
#     if forwarded_for and name == '127.0.0.1':
#         name = forwarded_for
#     msg = create_message(name, request.POST.get('body'))
#     cache.append(msg)
#     if len(cache) > cache_size:
#         cache = cache[-cache_size:]
#     new_message_event.set()
#     new_message_event.clear()
#     return msg

# @app.route('/a/message/updates', method='POST')
# def message_updates(session):
#     global cache
#     global new_message_event
#     cursor = session.get('cursor')
#     if not cache or cursor == cache[-1]['id']:
#          new_message_event.wait()
#     assert cursor != cache[-1]['id'], cursor
#     try:
#         for index, m in enumerate(cache):
#            if m['id'] == cursor:
#                return {'messages': cache[index + 1:]}
#         return {'messages': cache}
#     finally:
#         if cache:
#             session['cursor'] = cache[-1]['id']
#         else:
#             session.pop('cursor', None)

# def create_message(from_, body):
#     data = {'id': str(uuid.uuid4()), 'from': from_, 'body': body}
#     data['html'] = template('message', message=data)
#     return data
