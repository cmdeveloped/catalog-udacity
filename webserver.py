from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD
from database_setup import Base, Category, CategoryItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/categories/new"):
                categories = session.query(Category).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a New Category</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/categories/new' >"
                output += "<input name='newCategoryName' type='text' placeholder='New Category Name'>"
                output += "<input type='submit' value'Create'>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                categoryIDPath = self.path.split("/")[2]
                myCategoryQuery = session.query(Category).filter_by(
                    id=categoryIDPath).one()
                if myCategoryQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myCategoryQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/categories/%s/edit' >" % categoryIDPath
                    output += "<input name = 'newCategoryName' type='text' placeholder = '%s' >" % myCategoryQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    return

            if self.path.endswith("/categories"):
                categories = session.query(Category).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/categories/new'>Add a new category!</a><br><br>"
                for category in categories:
                    output += category.name
                    output += "</br><br>"
                    output += "<a href='/categories/%s/edit' >Edit</a>" % category.id
                    output += "</br>"
                    output += "<a href='/categories/%s/delete' >Delete</a>" % category.id
                    output += "</br><br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                categoryIDPath = self.path.split("/")[2]

                myCategoryQuery = session.query(Category).filter_by(id = categoryIDPath).one()
                if myCategoryQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output = "<html><body>"
                    output = "<h1>Are you sure you want to delete %s?" % myCategoryQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/categories/%s/delete' >" % categoryIDPath
                    output += "<input type='submit' value='delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newCategoryName')
                    categoryIDPath = self.path.split("/")[2]

                    myCategoryQuery = session.query(Category).filter_by(
                        id=categoryIDPath).one()
                    if myCategoryQuery != []:
                        myCategoryQuery.name = messagecontent[0]
                        session.add(myCategoryQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/categories')
                        self.end_headers()

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                categoryIDPath = self.path.split('/')[2]
                myCategoryQuery = session.query(Category).filter_by(id = categoryIDPath).one()

                if myCategoryQuery != []:
                    session.delete(myCategoryQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/categories')
                    self.end_headers()

            if self.path.endswith('/categories/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newCategoryName')

                # create categories
                newCategory = Category(name = messagecontent[0])
                session.add(newCategory)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/categories')
                self.end_headers()

            return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping server..."
        server.socket.close()

if __name__ == '__main__':
    main()
