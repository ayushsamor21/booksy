import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from db_operations.authors_operation import AuthorOperation

parser = argparse.ArgumentParser(description='API request to MySql Server')
parser.add_argument('-host', type=str, default='localhost', help='Server Host')
parser.add_argument('-port', type=int, default=8002, help='Server port')
parser.add_argument('-username', type=str, help='Your username')
parser.add_argument('-password', type=str, help='Your password')
parser.add_argument('-database', type=str, help='Your database')
args = parser.parse_args()

SERVER_HOST = args.host
SERVER_PORT = args.port

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class ApiHandler(BaseHTTPRequestHandler):

    @staticmethod
    def author_instance():
        return AuthorOperation(args.host, args.port, args.database, args.username, args.password)

    # def author_instance(self):
    #     self.author = AuthorOperation(args.host, args.port, args.database, args.username, args.password)

    def _set_headers(self, status = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def _get_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        return json.loads(body.decode('utf-8')) if body else {}

    def do_GET(self):
        if self.path == '/authors':
            authors = ApiHandler.author_instance().read_authors()
            self._set_headers()
            self.wfile.write(json.dumps(authors, default=str).encode('utf-8'))
        else:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == '/authors':
            body = self._get_request_body()
            name = body.get('name', 'unknown')
            description = body.get('description', 'No-description')
            email = body.get('email', 'No-email')
            author_id = self.author.insert_authors(name, description, email)
            self._set_headers(201)
            self.wfile.write(json.dumps({"id": author_id}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())


    def do_PUT(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 2 and path_parts[0] == "authors":
            try:
                author_id = int(path_parts[1])
            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"error": "Invalid ID"}')
                return

            body = self._get_request_body()
            name = body.get('name', 'unknown')
            description = body.get('description', 'No-description')
            email = body.get('email', 'No-email')
            self.author.update_authors(author_id, name, description, email)

            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Author updated"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Author not found"}).encode())

    def do_DELETE(self):
        path_parts = self.path.strip('/').split('/')
        if len(path_parts) == 2 and path_parts[0] == "authors":
            try:
                author_id = int(path_parts[1])
            except ValueError:
                self._set_headers(400)
                self.wfile.write(b'{"error": "Invalid ID"}')
                return

            self.author.delete_authors(author_id)
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": "Author deleted"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Author not found"}).encode())


def main():
        server_address = (SERVER_HOST, SERVER_PORT)
        httpd = HTTPServer(server_address, ApiHandler)
        print(f'Server running at http://{SERVER_HOST}:{SERVER_PORT}')
        httpd.serve_forever()

if __name__ == '__main__':
    main()
