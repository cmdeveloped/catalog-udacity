from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
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
        return redirect(url_for('mainCatalog', category_id=category_id))
    else:
        return render_template('newgame.html', category_id=category_id)

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET','POST'])
def editCategoryItem(category_id, item_id):
    editedItem = session.query(CategoryItem).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('mainCatalog', category_id = category_id))
    else:
        return render_template('editgame.html', category_id = category_id, item_id = item_id, i = editedItem)

@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET','POST'])
def deleteCategoryItem(category_id, item_id):
    deletedItem = session.query(CategoryItem).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('mainCatalog', category_id = category_id))
    else:
        return render_template('deletegame.html', i = deletedItem)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
