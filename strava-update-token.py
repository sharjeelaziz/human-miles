#!/usr/bin/python
# -*- coding: utf-8 -*-
import stravalib
import http.server
import urllib.parse
import webbrowser
import datetime

import config as c

port = 5000
url = 'http://localhost:%d/authorized' % port

client_id = c.get_setting(c.SECTION_SETTINGS, c.CLIENT_ID)
client_secret = c.get_setting(c.SECTION_SETTINGS, c.CLIENT_SECRET)

# Create the strava client, and open the web browser for authentication
client = stravalib.client.Client()
authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)
print('Opening: %s' % authorize_url)
webbrowser.open(authorize_url)


# Define the web functions to call from the strava API
def use_code(code):

    token_response = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)

    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']

    c.update_setting(c.SECTION_SETTINGS, c.ACCESS_TOKEN, access_token)
    c.update_setting(c.SECTION_SETTINGS, c.REFRESH_TOKEN, refresh_token)
    c.update_setting(c.SECTION_SETTINGS, c.EXPIRES_AT, str(expires_at))

    return client


class MyHandler(http.server.BaseHTTPRequestHandler):
    # Handle the web data sent from the strava API

    def do_HEAD(self):
        return self.do_get()

    def do_GET(self):
        # Get the API code for Strava
        self.wfile.write(b'<script>window.close();</script>')
        code = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['code'][0]
        print(code)

        # Login to the API
        client = use_code(code)


if __name__=='__main__':
    # Run the program to login and grab data
    try:
        httpd = http.server.HTTPServer(('localhost', port), MyHandler)
        httpd.handle_request()
    except KeyboardInterrupt:
                    # Allow ^C to interrupt from any thread.
                    sys.stdout.write('\033[0m')
                    sys.stdout.write('User Interrupt\n')
