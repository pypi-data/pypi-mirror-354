# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de

import logging

import click  # type: ignore
import os

from flask import Flask, render_template, session  # type: ignore
from flask_json import FlaskJSON  # type: ignore

from tgp_backend.project import Project

from tgp_backend.auth import SecretKeyManager
from tgp_backend.nextcloud import Nextcloud
from tgp_backend.config import LOG_LEVEL, MAIN_PATH, get_config_value

from .routes.project import project_routes
from .routes.views import main_views
from .routes.data import data_routes
from .routes.tabs import tab_manager
from .routes.collection import collection_routes
from .routes.publication import publication_routes

log = logging.getLogger(__name__)

base_params = {
    "title": "TG Prepare",
}

app = Flask(__name__)
FlaskJSON(app)

secret_manager = SecretKeyManager(MAIN_PATH)
app.secret_key = secret_manager.secret_key

# Additional security settings, if not in DEBUG mode
app.config.update(SESSION_COOKIE_NAME="tgp_session")
if LOG_LEVEL != "DEBUG":
    app.config.update(
        SESSION_COOKIE_SECURE=True,  # Only allow cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to cookies
        SESSION_COOKIE_SAMESITE="Strict",  # Protect against CSRF attacks
    )


app.register_blueprint(main_views)
app.register_blueprint(project_routes)
app.register_blueprint(data_routes)
app.register_blueprint(tab_manager)
app.register_blueprint(collection_routes)
app.register_blueprint(publication_routes)


def get_textgrid_login_url(instance):
    """
    Returns the TextGrid login URL based on the instance (test or production).
    """
    if instance == "test":
        return "https://test.textgridlab.org/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance=test.textgridlab.org"
    else:
        return "https://textgridlab.org/1.0/Shibboleth.sso/Login?target=/1.0/secure/TextGrid-WebAuth.php?authZinstance=textgrid-esx2.gwdg.de"


def get_projects():
    projects = []
    for sub in os.listdir(MAIN_PATH):
        projectpath = "%s/%s" % (MAIN_PATH, sub)
        if os.path.isdir(projectpath):
            projects.append(Project(sub))
    return projects


app.jinja_env.globals.update(
    len=len,
    round=round,
    title="TG Prepare",
    get_projects=get_projects,
    get_textgrid_login_url=get_textgrid_login_url,
)


def _startup():

    # Create the projects directory if it does not exist
    if not os.path.exists(MAIN_PATH):
        os.makedirs(MAIN_PATH)

    logging.getLogger("zeep").setLevel(logging.INFO)
    app.run(
        host=get_config_value("main", "host", default="0.0.0.0"),
        port=get_config_value("main", "port", default=8077),
        debug=get_config_value("log", "level", default="DEBUG") == "DEBUG",
    )


@click.command()
@click.option("--path", "-p", default=None)
def startup(path):
    base_params["path"] = path if path else os.getcwd()
    _startup()


# Step 9
@app.route("/tab-final-upload/<string:projectname>", methods=["GET"])
def tab_final_upload(projectname):
    # Erstelle das Project-Objekt
    project = Project(projectname)

    # Übergib das Project-Objekt an das Template
    return render_template(
        "tab_final_upload.html",
        project=project,  # Das Project-Objekt wird hier übergeben
    )


@app.route("/nextcloud_tab/", methods=["POST"])
def nextcloud_tab():
    nextcloud = Nextcloud(**session)
    return render_template(
        "nxc_tab.html",
        nextcloud=nextcloud if nextcloud.test_connection() else None,
        user=session.get("username", "-"),
    )


if __name__ == "__main__":
    startup()
