import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health': self.respond(200, {'status': 'ok'})
        elif self.path == '/version': self.respond(200, {'service': 'secure-demo-api', 'version': os.getenv('APP_VERSION', '1.0.0')})
        else: self.respond(404, {'error': 'not found'})
    def respond(self, code, body):
        data = json.dumps(body).encode(); self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self, fmt, *args): print(fmt % args, flush=True)

def main(): ThreadingHTTPServer(('0.0.0.0', int(os.getenv('PORT', '8000'))), Handler).serve_forever()
if __name__ == '__main__': main()
