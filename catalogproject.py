import random
import string
import httplib2
import json
import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask import flash, session as login_session, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, UserData
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

engine = create_engine('sqlite:///catalogDB.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Return User if login Successful"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print login_session
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Return logout response"""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['email']
        del login_session['picture']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['access_token']
        del login_session['user_id']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    """Return user id after created"""
    newUser = UserData(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(UserData).filter_by(email=login_session[
        'email']).one()
    return user.id


def getUserInfo(user_id):
    """Return user if user in login_session matches with db record"""
    user = session.query(UserData).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Return id of user if user in login_session matches with db record"""
    try:
        user = session.query(UserData).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/')
@app.route('/home')
def allcategories():
    """Redirect to home page containing all categories and latest items"""
    categories = session.query(Category).all()
    latestitems = session.query(Item).order_by(Item.id.desc()).limit(3).all()
    return render_template(
        'home.html',
        categories=categories,
        latestitems=latestitems)


@app.route('/home/JSON')
def allcategoriesJSON():
    """Return JSON Endpoints for all categories"""
    categories = session.query(Category).all()
    latestitems = session.query(Item).order_by(Item.id.desc()).limit(3).all()
    return jsonify(latestitems=[i.serialize for i in latestitems])


@app.route('/categories/<int:category_id>/')
def categoryMenu(category_id):
    """Return items of respective category"""
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return render_template(
        'categoriesmenu.html',
        categories=categories,
        category=category,
        items=items)


@app.route('/categories/<int:category_id>/JSON')
def categoryMenuJSON(category_id):
    """Return JSON Endpoint for all categories"""
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/<int:item_id>')
def itemsMenu(category_id, item_id):
    """Return items of particular category"""
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id)

    if 'username' not in login_session:
        return render_template(
            'publicitemmenu.html',
            category=category,
            items=items)
    else:
        return render_template(
            'itemmenu.html',
            category=category,
            items=items)


@app.route('/categories/<int:category_id>/<int:item_id>/JSON')
def itemsMenuJSON(category_id, item_id):
    """Return JSON Endpoints for all items of category"""
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(id=item_id)
    if 'username' not in login_session:
        return jsonify(items=[i.serialize for i in items])
    else:
        return jsonify(items=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    """Redirect to newitem page to create new item otherwise to categoryMenu"""
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        return "You are not authorized to add menu items to this"
    if request.method == 'POST':
        user_id = login_session['email']
        newItem = Item(
            title=request.form['name'],
            description=request.form['description'],
            category_id=category_id,
            user_id=category.user_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template(
            'newitem.html',
            category_id=category_id)


@app.route(
    '/categories/<int:category_id>/<int:item_id>/edit/',
    methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """Redirect to edit item page if user is authorized else to categoryMenu"""
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return "You are not authorized to edit this item"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.title = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template(
            'edititem.html',
            category_id=category_id,
            item_id=item_id,
            i=editedItem)


@app.route('/categories/<int:category_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """Redirect to deleteItem page if useris authorized"""
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != itemToDelete.user_id:
        return "You are not authorized to delete menu items."
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template(
            'deleteitem.html',
            item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
