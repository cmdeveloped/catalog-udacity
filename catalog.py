from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

# Import for Secure Access
from flask import session as login_session
import random, string

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Creating a state token to prevent request forgery
# Storing said token in the flask session for later validation from user
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return "This session's state is: %s" %login_session['state']

# JSON routes / API Endpoint using a GET request
@app.route('/catalog/<int:category_id>/games/JSON')
def catalogGamesJSON(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CategoryItem).filter_by(category_id = category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])

@app.route('/catalog/<int:category_id>/game/<int:game_id>/JSON')
def catalogGameJSON(category_id, game_id):
    catalogGame = session.query(CategoryItem).filter_by(id = game_id).one()
    return jsonify(CatalogGame = catalogGame.serialize)

@app.route('/')
@app.route('/catalog/')
def mainView():
    catalog = session.query(Category).all()
    return render_template('catalog.html', catalog = catalog)

@app.route('/catalog/<int:category_id>/')
def mainCatalog(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CategoryItem).filter_by(category_id = category.id)
    return render_template('catalog.html', category = category, items = items)

@app.route('/catalog/<int:category_id>/new/', methods=['GET','POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        newGame = CategoryItem(name = request.form['name'], category_id = category_id)
        session.add(newGame)
        session.commit()
        flash('New Game Created!')
        return redirect(url_for('mainCatalog', category_id=category_id))
    else:
        return render_template('newgame.html', category_id=category_id)

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET','POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('Game has been edited!')
        return redirect(url_for('mainCatalog', category_id = category_id))
    else:
        return render_template('editgame.html', category_id = category_id, item_id = item_id, i = editedItem)

@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET','POST'])
def deleteCategoryItem(category_id, item_id):
    deletedItem = session.query(CategoryItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash('Game has been deleted!')
        return redirect(url_for('mainCatalog', category_id = category_id))
    else:
        return render_template('deletegame.html', i = deletedItem)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
