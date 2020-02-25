import socket
import pathlib
from http.server import *
from utils.ip_port import formatted_address

_data_dir: pathlib.Path


class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def main_html(self):
        _INDEX_HTML = '''
                    <html>
                        <body>
                            <ul>
                                {users}
                            </ul>
                        </body>
                    </html>
                    '''
        _USER_LINE_HTML = '''
                        <li><a href="/users/{user_id}">user {user_id}</a></li>
                          '''
        users_html = []
        for user_dir in _data_dir.iterdir():
            users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
        index_html = _INDEX_HTML.format(users='\n'.join(users_html))

        return index_html.encode("utf8")  # NOTE: must return a bytes object!

    def user_html(self):
        splitted_path = self.path.split("/")

        if len(splitted_path) != 3:
            return "<html> <body> <p> Wrong path! </p> </body> </html>".encode("utf8")
        
        current_path = pathlib.Path(str(_data_dir) + "/" + splitted_path[2])
        
        if not current_path.is_dir():
            return "<html> <body> <p> Wrong path! </p> </body> </html>".encode("utf8")

        _INDEX_HTML = '''
                    <html>
                        <head>
                            <title> Brain Computer Interface: User {user_num} </title>
                        </head>
                        <body>
                            <table>
                                {thoughts}
                            </table>
                        </body>
                    </html>
                    '''
        _THOUGHT_LINE_HTML = '''
                        <tr>
                            <td> {file_name} </td>
                            <td> {data} </td>
                        </tr>
                          '''

        #TODO: refactor ugly code!
        thoughts_html = []
        for thought_file in current_path.iterdir():
            splitted_time    = thought_file.stem.split("_")
            splitted_time[1] = splitted_time[1].replace("-", ":")
            thoughts_html.append(_THOUGHT_LINE_HTML.format(file_name=str(splitted_time[0] + " " + splitted_time[1]), data=thought_file.read_text()))
        index_html = _INDEX_HTML.format(thoughts='\n'.join(thoughts_html), user_num=splitted_path[2])
        
        return index_html.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        to_write = ""
        if self.path == "/" or self.path == "/favicon.ico":
            to_write = self.main_html()
        else:
            to_write = self.user_html()
        
        self.wfile.write(to_write)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))


def run_webserver(address, data_dir):
    global _data_dir
    _data_dir = data_dir
    httpd = HTTPServer((address[0], address[1]), RequestHandler)

    print(f"Starting httpd server on {address[0]}:{address[1]}")
    httpd.serve_forever()


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address  = argv[1]
        data_dir = pathlib.Path(argv[2])

        # IP:Port manipulation
        address = formatted_address(address)

        run_webserver(address, data_dir)
        
        print('done')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
