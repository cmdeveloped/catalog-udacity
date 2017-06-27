# Import main modules
from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

# Import for Secure Access
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json

from flask import make_response
import requests

# JSON Client Secret from google developer
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creating a state token to prevent request forgery
# Storing said token in the flask session for later validation from user
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Create a route for google connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    credentials = AccessTokenCredentials(
        login_session['credentials'], 'user-agent-value')
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user.', 200))

    # Get user info from google.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Storing the users information to return a welcome message.
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px; border-radius: 100%;'
    output += '-webkit-border-radius: 100%;-moz-border-radius: 100%;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Application route to disconnect the user logged in and revoke access to certain features.
@app.route('/gdisconnect/')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = login_session['credentials']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # If the result is good, deleting users information
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON routes / API Endpoint using a GET request
@app.route('/catalog/<int:category_id>/games/JSON')
def catalogGamesJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(
        CategoryItem).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/game/<int:game_id>/JSON')
def catalogGameJSON(category_id, game_id):
    catalogGame = session.query(CategoryItem).filter_by(id=game_id).one()
    return jsonify(CatalogGame=catalogGame.serialize)


# Catalog main page route displays categories and flash messages
@app.route('/')
@app.route('/catalog')
def mainView():
    catalog = session.query(Category).all()
    return render_template('catalog.html', catalog=catalog)


# Route to view each category and its items
@app.route('/catalog/<int:category_id>/')
def eachCatalog(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    if 'username' not in login_session:
        return render_template('publiccategories.html', category=category, items=items)
    else:
        return render_template('categories.html', category=category, items=items)


# Route to create a new category item
@app.route('/catalog/<int:category_id>/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newGame = CategoryItem(
            name=request.form['name'], description=request.form['description'], genre=request.form['genre'], category_id=category_id, user_id=category.user_id)
        session.add(newGame)
        session.commit()
        flash('New Game Created!')
        return redirect(url_for('eachCatalog', category_id=category_id))
    else:
        return render_template('newgame.html', category_id=category_id)


# Route to edit category item
@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('Game title has been edited!')

        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Game description has been edited!')
        return redirect(url_for('eachCatalog', category_id=category_id))
    else:
        return render_template('editgame.html', category_id=category_id,
                               item_id=item_id, i=editedItem)


# Route to delete the category items
@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Game has been deleted!')
        return redirect(url_for('eachCatalog', category_id=category_id))
    else:
        return render_template('deletegame.html', i=deletedItem)


# Used the basic secret_key from udacity video
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
