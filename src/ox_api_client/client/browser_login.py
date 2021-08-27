import logging
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from random import randint

from ox_api_cli.client.client_core import OXApiClient


class BrowserLogin():
    def __init__(self, client: OXApiClient):
        self.client = client

    def interactive_login(self):
        done = False
        shelf = self.client

        class MyRequestHandler(SimpleHTTPRequestHandler):
            def do_GET(self):
                nonlocal done
                logging.debug(self.request)
                if self.path == '/redir':
                    # redirect the browser to the interactive login url
                    self.send_response(303)
                    self.send_header('Location', login_url)
                    logging.debug("REDIRECTING: %s", login_url)
                    self.end_headers()
                elif self.path.startswith('/cb'):
                    done = True

                    response = shelf._oauth_session.parse_authorization_response(self.path)
                    shelf.access_token = shelf._oauth_session.fetch_access_token(
                        shelf.base_authorization_url + '/api/index/token',
                        response['oauth_verifier'])

                    self.send_response(200, "OK")
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        '<body>Cool, you can close this tab'
                        '<script>window.close();</script>'
                        '</body>'.encode('utf-8'))
                else:
                    self.send_response(200, "OK")
                    self.end_headers()

        port = randint(1024, 65000)
        try:
            with HTTPServer(("0.0.0.0", port), MyRequestHandler) as httpd:
                logging.debug("Listening for browser connection on %s:%d", httpd.server_address, httpd.server_port)
                shelf.obtain_request_token('http://localhost:%d/cb' % httpd.server_port)
                login_url = shelf._oauth_session.authorization_url(shelf.base_authorization_url + '/login/login',
                                                                   shelf._request_token['oauth_token'])
                webbrowser.open("http://localhost:%d/redir" % httpd.server_port, 1)
                while True:
                    httpd.handle_request()
                    if done:
                        break

        except OSError as err:
            if err.errno == 98:  # address already in use
                port += 1
            else:
                raise
        print("Done")
