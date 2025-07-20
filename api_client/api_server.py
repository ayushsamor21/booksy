import argparse
import mysql.connector
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

parser = argparse.ArgumentParser(description='API request to MySql Server')
parser.add_argument('-host', type=str, default='localhost', help='Server Host')
parser.add_argument('-port', type=int, default=8002, help='Server port')
parser.add_argument('-username', type=str, help='Your username')
parser.add_argument('-password', type=str, help='Your password')
parser.add_argument('-database', type=str, help='Your database')
args = parser.parse_args()

mydb = mysql.connector.connect(
    host = 'localhost',
    user = args.username,
    password = args.password,
    database = args.database
)

SERVER_HOST = args.host
SERVER_PORT = args.port


def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


class SampleApiHandler(BaseHTTPRequestHandler):

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
            cursor = mydb.cursor()
            cursor = mydb.cursor(dictionary=True)
            cursor.execute('SELECT * FROM authors')
            authors = cursor.fetchall()
            cursor.close()

            self._set_headers()
            self.wfile.write(json.dumps(authors, default=str).encode('utf-8'))

        else:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def do_POST(self):
        if self.path == '/authors':
            cursor = mydb.cursor()
            body = self._get_request_body()
            cursor.execute("""
                           INSERT INTO authors (name, description, email, created_by, updated_by, status)
                           VALUES (%s, %s, %s, %s, %s, %s)
                       """, (
                body.get('name', 'Unnamed'),
                body.get('description', 'No-description'),
                body.get('email', 'noemail@example.com'),
                0, 0, 'active'
            ))
            mydb.commit()
            inserted_id = cursor.lastrowid
            cursor.close()
            mydb.close()

            self._set_headers(201)
            self.wfile.write(json.dumps({"id": inserted_id}).encode())
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
            cursor = mydb.cursor()
            cursor.execute("""
                UPDATE authors
                SET name=%s, description=%s, email=%s, updated_by=%s, updated_at=%s
                WHERE id=%s
            """, (
            body.get('name'),
            body.get('description'),
            body.get('email'),
            0,
            datetime.now(),
            author_id
        ))

            mydb.commit()
            cursor.close()
            mydb.close()


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

            cursor = mydb.cursor()
            cursor.execute("DELETE FROM authors WHERE id = %s", (author_id,))
            mydb.commit()
            affected = cursor.rowcount
            cursor.close()
            mydb.close()

            if affected:
                self._set_headers(200)
                self.wfile.write(json.dumps({"message": "Author deleted"}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Author not found"}).encode())


def main():
        server_address = (SERVER_HOST, SERVER_PORT)
        httpd = HTTPServer(server_address, SampleApiHandler)
        print(f'Server running at http://{SERVER_HOST}:{SERVER_PORT}')
        httpd.serve_forever()

if __name__ == '__main__':
    main()




