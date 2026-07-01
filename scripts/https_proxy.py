#!/usr/bin/env python3
"""HTTPS reverse proxy for Ollama — no external dependencies."""

import ssl, os, urllib.request, urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

BACKEND  = os.environ.get("BACKEND", "http://localhost:11434")
PORT     = int(os.environ.get("PORT", "8443"))
DOMAIN   = os.environ.get("DOMAIN", "4ride.online")
SSL_DIR  = os.path.join(os.path.dirname(__file__), "ssl")
CERT     = os.path.join(SSL_DIR, "fullchain.pem")
KEY      = os.path.join(SSL_DIR, "key.pem")
DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "devweb", "dist")

SKIP_HEADERS = {'host', 'connection', 'transfer-encoding', 'keep-alive'}

MIME = {
    '.html': 'text/html; charset=utf-8',
    '.js':   'application/javascript',
    '.css':  'text/css',
    '.png':  'image/png',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
    '.json': 'application/json',
}

class ProxyHandler(BaseHTTPRequestHandler):
    def serve_static(self):
        path = self.path.split('?')[0]
        if path == '/':
            path = '/index.html'
        file_path = os.path.normpath(os.path.join(DIST_DIR, path.lstrip('/')))
        if not file_path.startswith(os.path.abspath(DIST_DIR)):
            self.send_response(403); self.end_headers(); return
        if not os.path.isfile(file_path):
            # SPA fallback
            file_path = os.path.join(DIST_DIR, 'index.html')
        ext = os.path.splitext(file_path)[1]
        mime = MIME.get(ext, 'application/octet-stream')
        with open(file_path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def proxy_api(self):
        url = BACKEND + self.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items() if k.lower() not in SKIP_HEADERS}
        headers['Host'] = 'localhost'
        req = urllib.request.Request(url, data=body, headers=headers, method=self.command)
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in SKIP_HEADERS:
                        self.send_header(k, v)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self.end_headers(); self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502); self.end_headers(); self.wfile.write(f"Proxy error: {e}".encode())

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_api()
        else:
            self.serve_static()

    def do_POST(self):   self.proxy_api()
    def do_OPTIONS(self): self.proxy_api()
    def do_HEAD(self):   self.proxy_api()
    def do_PUT(self):    self.proxy_api()
    def do_DELETE(self): self.proxy_api()

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} → {args[0]} {args[1]}")


def gen_cert():
    os.makedirs(SSL_DIR, exist_ok=True)
    ret = os.system(
        f'openssl req -x509 -newkey rsa:2048 -keyout "{KEY}" -out "{CERT}" '
        f'-days 365 -nodes -subj "/CN={DOMAIN}" 2>/dev/null'
    )
    if ret != 0:
        raise RuntimeError("openssl failed — is openssl installed?")


if __name__ == '__main__':
    if not os.path.exists(CERT) or not os.path.exists(KEY):
        print("[*] Generating self-signed certificate...")
        gen_cert()
        print(f"[*] Certificate saved to {SSL_DIR}/")

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT, KEY)

    server = ThreadedHTTPServer(('0.0.0.0', PORT), ProxyHandler)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    print(f"[*] HTTPS proxy: https://0.0.0.0:{PORT} → {BACKEND}")
    print(f"[*] Public URL: https://{DOMAIN} (after router change 443 → {PORT})")
    print("[*] Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopped.")
