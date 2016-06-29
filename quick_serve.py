# This file provided by Facebook is for non-commercial testing and evaluation purposes only.
# Facebook reserves all rights not expressly granted.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
from flask import Flask, Response, request, jsonify, current_app, make_response
from datetime import timedelta
from functools import update_wrapper

from OpenSSL import SSL

# context = SSL.Context(SSL.SSLv23_METHOD)
# context.use_privatekey_file('key.pem')
# context.use_certificate_file('cert.pem')
context = ('cert.pem', 'key.pem')

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/comments.json', methods=['GET', 'POST'])
def comments_handler():

    with open('comments.json', 'r') as file:
        comments = json.loads(file.read())

    ## got it -- can accept new comments and caches them to local file. smooth
    if request.method == 'POST':
        comments.append(request.form.to_dict())

        with open('comments.json', 'w') as file:
            file.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(json.dumps(comments), mimetype='application/json', headers={'Cache-Control': 'no-cache'})

@app.route('/track')
def trackz():
	print("horoay")
	return "yes"

@app.route("/v1/p", methods=['POST'])
def page():
    print('hooray')
    print(request.data)
    return "yes"

@app.route("/v1/t", methods=['POST'])
def track():
    print('track event')
    print(request.data)
    return "yes"

@app.route("/p",methods=['POST'])
@crossdomain(origin='*')
def success():
    return jsonify(success=True)

@app.route("/g", methods=['POST'])
@crossdomain(origin='*')
def g():
    return jsonify(success=True)

@app.route("/a", methods=['POST'])
@crossdomain(origin='*')
def a():
    return jsonify(success=True)

@app.route("/i", methods=['POST'])
@crossdomain(origin='*')
def i():
    return jsonify(success=True)

@app.route("/t", methods=['POST'])
@crossdomain(origin='*')
def t():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT",4000)))
