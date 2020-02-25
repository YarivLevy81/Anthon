from http.server import *
from functools import wraps
import re


class Website:

    routes = {}
    
    def route(self, path):
        def decorator(f):
            
            if path not in self.routes:
                self.routes[path] = f
            @wraps(f)
            
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        
        return decorator

    def run(self, address): 
        httpd = HTTPServer(address, Website.RequestHandler)
        httpd.serve_forever()

    class RequestHandler(BaseHTTPRequestHandler):

        def _set_headers(self, code):
            self.send_response(code)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            module   = None
            err      = True
            re_group = None
            for route, func in Website.routes.items():
                re_group = re.fullmatch(route, self.path)
                if re_group:
                    err    = False
                    module = func
                    break
                
            to_write = ""
            if err:
                to_write = "".encode("utf8")
                self._set_headers(404)
                
            else:
                to_write = module(*re_group.groups())
                self._set_headers(to_write[0])
                to_write = to_write[1].encode("utf8")
            
            self.wfile.write(to_write)
