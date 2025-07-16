from http.server import BaseHTTPRequestHandler, HTTPServer
import json

authors = []

HOST = 'localhost'
PORT = 8002

class SampleApiHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/authors":
            self._set_headers()
            output = json.dumps(authors)
            self.wfile.write(output.encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode())


    def _get_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        return json.loads(body.decode('utf-8')) if body else {}

    def do_POST(self):
        if self.path == '/authors':
            body = self._get_request_body()
            author_id = len(authors) + 1
            author = {
                'id': author_id,
                'name': body.get('name', 'Unnamed authors'),
                'city': body.get('city', 'unknown city')
            }
            authors.append(author)
            self._set_headers(201)
            self.wfile.write(json.dumps(author).encode())
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not found"}')

    def do_PUT(self):
        author_id = self.path.split('/')[-1]
        author_exists = False
        for author in authors:
            if author['id'] == int(author_id):
                author_exists = True
                body = self._get_request_body()
                body['id'] = author_id

                # change in data store
                author['name'] = body['name']
                author['city'] = body['city']
                self._set_headers(200)
                self.wfile.write(json.dumps(author).encode())
                break

            if not author_exists:
                self._set_headers(404)
                self.wfile.write(b'{"error": "Not found"}')

    def do_DELETE(self):
        author_id = self.path.split('/')[-1]
        author_exists = False
        for author in authors:
            if author['id'] == int(author_id):
                author_exists = True
                authors.remove(author)
                self._set_headers(202)
                break
        if not author_exists:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not found"}')

def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, SampleApiHandler)
    print(f"Starting sever on http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

