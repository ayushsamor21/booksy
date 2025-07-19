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


def main():
        server_address = (SERVER_HOST, SERVER_PORT)
        httpd = HTTPServer(server_address, SampleApiHandler)
        print(f'Server running at http://{SERVER_HOST}:{SERVER_PORT}')
        httpd.serve_forever()

if __name__ == '__main__':
    main()




