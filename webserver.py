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
            if self.path.endswith('/categories'):
                categories = session.query(Category).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                for category in categories:
                    output += category.name
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

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
