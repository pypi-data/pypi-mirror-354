# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de

import logging

from flask import Blueprint, render_template, request
from flask_json import json_response

from tgp_backend.project import Project, TGProject

log = logging.getLogger(__name__)

publication_routes = Blueprint("publication", __name__)


@publication_routes.route(
    "/tab-prepare-upload/<string:projectname>", methods=["GET"]
)
def tab_upload(projectname):
    project = Project(projectname)

    return render_template(
        "tabs/upload.html",
        project=project,
    )


# ***TAB CHECK RESULTS***
# ***********************
@publication_routes.route(
    "/tab-check-result/<string:projectname>", methods=["GET"]
)
def tab_check_result(projectname):
    # Erstelle das Project-Objekt
    project = Project(projectname)

    # Übergib das Project-Objekt an das Template
    return render_template(
        "tabs/check_result.html",
        project=project,  # Das Project-Objekt wird hier übergeben
    )


class TGProjectHandler:
    def __init__(self, projectname, instance):
        self.project = Project(projectname)
        self.tg_project = self.project.get_tgp(instance)
        self.instance = instance

    def _render_template(self):
        return render_template(
            "includes/upload_form.html",
            project=self.project,
            instance=self.instance,
        )

    def save_session_id(self, session_id):
        self.tg_project.tg_session_id = session_id
        return self._render_template()

    def save_tg_project_id(self, tg_project_id):
        self.tg_project.tg_project_id = tg_project_id
        return self._render_template()

    def delete_tg_project(self, tg_project_id):
        self.tg_project.delete_tg_project(tg_project_id)
        return self._render_template()

    def create_tg_project(self, tg_projectname):
        self.tg_project.create_tg_project(tg_projectname)
        return self._render_template()


@publication_routes.route(
    "/save_session_id/<string:projectname>/<string:instance>", methods=["POST"]
)
def save_session_id(projectname, instance):
    return TGProjectHandler(projectname, instance).save_session_id(
        request.form.get("tg_auth_session_id")
    )


@publication_routes.route(
    "/save_tg_project_id/<string:projectname>/<string:instance>/<string:tg_project_id>",
    methods=["POST"],
)
def save_tg_project_id(projectname, instance, tg_project_id):
    return TGProjectHandler(projectname, instance).save_tg_project_id(
        tg_project_id
    )


@publication_routes.route(
    "/delete_tg_project_id/<string:projectname>/<string:instance>/<string:tg_project_id>",
    methods=["POST"],
)
def delete_tg_project_id(projectname, instance, tg_project_id):
    return TGProjectHandler(projectname, instance).delete_tg_project(
        tg_project_id
    )


@publication_routes.route(
    "/create_tg_project/<string:projectname>/<string:instance>",
    methods=["POST"],
)
def create_tg_project(projectname, instance):
    return TGProjectHandler(projectname, instance).create_tg_project(
        request.form.get("tg_projectname")
    )


@publication_routes.route(
    "/upload_project/<string:projectname>/<string:instance>", methods=["POST"]
)
def upload_project(projectname, instance):
    TGProject(projectname, instance).upload_tg_project()
    return json_response(response="OK")


# @publication_routes.route(
#     "/get_tg_project_hits/<string:projectname>/<string:instance>/<string:tg_project_id>",
#     methods=["GET"],
# )
# def get_tg_project_hits(projectname, instance, tg_project_id):
#     hits = TGProject(projectname, instance).get_tg_project_hits(tg_project_id)
#     return json_response(response="OK", hits=hits)
