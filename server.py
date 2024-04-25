from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # إذا كان المسار هو الجذر، أرسل صفحة تسجيل الدخول
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('login.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            # إذا كان المسار غير الجذر، أرسل الملف المطلوب إذا كان موجودًا
            try:
                file_path = '.' + self.path
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # تحويل بيانات POST إلى قاموس
        post_dict = urllib.parse.parse_qs(post_data)

        # التحقق من صحة اسم المستخدم وكلمة المرور
        if post_dict.get('username', [''])[0] == 'admin' and post_dict.get('password', [''])[0] == 'password':
            response_content = 'Login Successful'
        else:
            response_content = 'Invalid Username or Password'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<html><body><h1>{response_content}</h1></body></html>".encode())

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server(8000)

