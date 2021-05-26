import os
import time

from flask import Flask, url_for, session, render_template, request, send_file, flash
from flask_oidc import OpenIDConnect
from werkzeug.utils import redirect

from dash.network import GetAll
from dash.plotly_dashboard import create_plot
from database.database import base
from database.repository.directory_repository import DirectoryRepository
from database.repository.files_repository import FilesRepository
from tools.manager import Manage
from md5change import md5
from configuration import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hardsecretkey'
app.config.from_mapping(
    SECRET_KEY=OAUTH_SECRET_KEY,
    OIDC_CLIENT_SECRETS=OAUTH_OIDC_CLIENT_SECRETS,
    OIDC_VALID_ISSUERS=OAUTH_OIDC_VALID_ISSUERS,
    OIDC_INTROSPECTION_AUTH_METHOD=OAUTH_OIDC_INTROSPECTION_AUTH_METHOD,
    OIDC_SCOPES=OAUTH_OIDC_SCOPES,
    OIDC_CLOCK_SKEW=OAUTH_OIDC_CLOCK_SKEW,
    OIDC_ID_TOKEN_COOKIE_SECURE=OAUTH_OIDC_ID_TOKEN_COOKIE_SECURE,
)

oidc = OpenIDConnect(app)


@app.before_request
def _db_connect():
    base.connect()


@app.teardown_request
def _db_close(exc):
    if not base.is_closed():
        base.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
@oidc.require_login
def index_get():
    if oidc.user_loggedin:
        user_role = oidc.get_cookie_id_token()
        displayAllDirectory = DirectoryRepository().getAll(user_role['roles'][0])
        return render_template('index.html', get_user=oidc.user_getfield('preferred_username'),
                               displayAllDirectory=displayAllDirectory)
    else:
        render_template('/errors/403.html'), 403


@app.route("/", methods=['POST'])
@oidc.require_login
def index_post():
    if oidc.user_loggedin:
        user_role = oidc.get_cookie_id_token()
        newDirectoryName = request.form["name"]
        if user_role['roles'][0] == "RSA_ADMIN":
            create_dict = {"Name": newDirectoryName}
            DirectoryRepository().createOne(create_dict)
            return redirect("/")
    else:
        return render_template('/errors/403.html'), 403
    return redirect("/")


@app.route("/dashboard/", methods=['POST'])
def dashboard_post():
        network = request.form["network"]
        bar = create_plot(network)
        network = GetAll()
        return render_template('dashboard.html', network=network, plot=bar)

@app.route("/dashboard/", methods=['GET'])
def dashboard_get():
    network = GetAll()
    return render_template('dashboard.html',network=network)


@app.route('/directory/<Id>', methods=['GET'])
def directories_get(Id):
    if oidc.user_loggedin:
        displayAllFiles = FilesRepository().getAll(Id)
        # displayCurrentDirectory = DirectoryRepository().getOne(Id)
        return render_template('templatefiles.html', get_user=oidc.user_getfield('preferred_username'),
                               displayAllFiles=displayAllFiles)
    else:
        return render_template('/errors/403.html'), 403


@app.route('/directory/<Id>', methods=['POST'])
def directories_post(Id):
    user = oidc.user_getfield('preferred_username')
    f = request.files['file']
    if f and allowed_file(f.filename):
        Manage().directorymanager()
        Manage().filemanager(f)
        f.seek(1, os.SEEK_END)
        length = f.tell()
        file_length = round((length / 1024) / 1024, 2)  # oblicza filesize z requesta
        create_dict = {'name': f.filename,
                       'path': Manage().directorymanager()[1] + os.sep + md5.name,
                       'filesize': file_length,
                       'creationdate': Manage().directorymanager()[2],
                       "directoryId": Id, "username": user}
        FilesRepository().createOne(create_dict)
        return redirect('/directory/' + Id)
    else:
        flash('Próbowano wgrać niedozwolony plik.')
        return redirect('/directory/' + Id)


@app.route('/download/<Id>', methods=['GET'])
def download(Id):
    if oidc.user_loggedin:
        getFile = FilesRepository().getOne(Id)
        row = getFile[0]
        return send_file(row.path, as_attachment=True, attachment_filename=row.name)
    else:
        return render_template('/errors/403.html'), 403


@app.route('/delete/<Id>', methods=['GET'])
def deletefile(Id):
    if oidc.user_loggedin:
        getfile = FilesRepository().getOne(Id)
        os.remove(getfile[0].path)
        FilesRepository().clearOne(Id)
        return redirect('/directory/' + str(getfile[0].directoryId))
    else:
        return render_template('/errors/403.html'), 403


@app.route("/logout/", methods=['GET'])
def logout():
    session.pop('expires_in', 0)
    session.pop('timer', 0)
    session.pop('csrf_token', '')
    return redirect(url_for('/'))


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('/errors/404.html'), 404


app.register_error_handler(404, pageNotFound)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('/errors/500.html'), 500


app.register_error_handler(500, internal_server_error)
if __name__ == "__main__":
    app.run(debug=False)
