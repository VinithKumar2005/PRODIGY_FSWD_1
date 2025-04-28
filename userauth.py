from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file("index.html", content_type="text/html")
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode()
            data = parse_qs(body)
            username = data.get('username', [''])[0]
            password = data.get('password', [''])[0]

            if username and password:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Welcome</title>
                        <style>
                            body {{
                                margin: 0;
                                padding: 0;
                                font-family: 'Segoe UI', sans-serif;
                                background: linear-gradient(to right, #43cea2, #185a9d);
                                height: 100vh;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                            }}
                            .box {{
                                background-color: rgba(0, 0, 0, 0.4);
                                padding: 40px;
                                border-radius: 15px;
                                text-align: center;
                                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                            }}
                            h1 {{
                                font-size: 36px;
                                margin-bottom: 10px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="box">
                            <h1>Welcome {username}</h1>
                            <p>You are logged in successfully.</p>
                        </div>
                    </body>
                    </html>
                """, "utf-8"))
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Login Failed</title></head>
                    <body style="font-family: sans-serif; background: #f8d7da; color: #721c24; text-align: center; padding-top: 100px;">
                        <h2>Login Failed</h2>
                        <p>Username or password missing. Please go back and try again.</p>
                    </body>
                    </html>
                """)

    def serve_file(self, filename, content_type="text/plain"):
        try:
            with open(filename, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, f"{filename} not found.")

PORT = 8000
print(f"Server running at http://localhost:{PORT}")
server = HTTPServer(("localhost", PORT), SimpleHandler)
server.serve_forever()
