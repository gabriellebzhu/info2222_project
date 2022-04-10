'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''


from re import S
import bottle
from bottle import route, get, post, error, request, response, static_file, hook
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
    user_pk = request.json.get('user_pk')
    print(username)
    print(password)
    print(user_pk)
    
    # Call the appropriate method
    check = model.login_check(username, password)

    if check[0]:
        print("ok!")
        print(check[1])
        response.set_cookie("account", username, secret=sec.COOKIE_SECRET)
        responding_msg = {'message': 'successful login', 'success':'1'}

    else:
        responding_msg = {'message': 'bad login', 'success':'0'}

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
    print(output)  # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output)  # this converts the json output to a python dictionary
    print(result)  # Printing the new dictionary
    print(type(result))  # this shows the json converted as a python dictionary
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
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Call the appropriate method
    return model.register_new_user(username, password)


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


@app.route('/chat/<friend_id>')
def get_chat_with_friend(friend_id):
    username = request.get_cookie("account", secret=sec.COOKIE_SECRET)

    return model.friend_chat(username, friend_id)


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
