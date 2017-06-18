from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

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

@app.route('/catalog/<int:category_id>/new/')
def newCategoryItem(category_id):
    return "Page to create a new Category Item."

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editCategoryItem(category_id, item_id):
    return "Page to edit a menu item."

@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteCategoryItem(category_id, item_id):
    return "Page to delete a menu item."


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
