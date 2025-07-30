# -*- coding: utf-8 -*-
# Copyright (C) 2023,2024 TU-Dresden (ZIH)
# ralf.klammer@tu-dresden.de
# moritz.wilhelm@tu-dresden.de
import logging

from tgadmin.tgimport import aggregation_import
from tgadmin.tgadmin import _crud_delete_op

from tgclients import (
    TextgridAuth,
    TextgridConfig,
    TextgridCrud,
    TextgridSearch,
)
from tgclients.config import PROD_SERVER, TEST_SERVER

log = logging.getLogger(__name__)


class TGclient(object):
    def __init__(self, sid, instance="test", verbose=False):
        self.sid = sid

        if instance == "live":
            self.server = PROD_SERVER
        else:
            self.server = TEST_SERVER
        self.config = TextgridConfig(self.server)

        self.crud = TextgridCrud(self.config)
        self.tgauth = TextgridAuth(self.config)
        self.tgsearch = TextgridSearch(self.config, nonpublic=True)

    def create_project(self, name, description=""):
        log.info(f"Creating project {name}")
        return self.tgauth.create_project(self.sid, name, description)

    def delete_project(self, project_id):
        log.info(f"Deleting project {project_id}")
        content = self.get_project_content(project_id)

        # delete content of project
        # repeat until whole content has been deleted
        # (necessary because of default limit in '_crud_delete_op')
        while int(content.hits) > 0:
            for tgobj in content.result:
                _crud_delete_op(self, tgobj)
            content = self.get_project_content(project_id)

        return self.tgauth.delete_project(self.sid, project_id)

    def get_project_content(self, project_id):
        contents = self.tgsearch.search(
            filters=["project.id:" + project_id], sid=self.sid
        )
        return contents

    def get_assigned_projects(self):
        log.info("Listing assigned projects")
        # TODO: this needs a better error handling to indicate user,
        # that the session-id seeems to be invalid
        try:
            _projects = self.tgauth.list_assigned_projects(self.sid)
        except Exception as e:
            log.error(f"Error listing assigned projects: {e}")
            return []

        for project_id in _projects:
            desc = self.tgauth.get_project_description(project_id)
            if desc:
                yield {
                    "id": project_id,
                    "name": desc.name,
                    "description": desc.description,
                    "contents": self.get_project_content(project_id).hits,
                }
            else:
                log.warning(
                    f"Cannot find project description for: {project_id}"
                )

    def put_aggregation(self, project_id, aggregation_file):
        res = aggregation_import(
            self.crud,
            self.sid,
            project_id,
            aggregation_file,
            threaded=True,
            ignore_warnings=True,
        )
