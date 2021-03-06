import datetime

from freezegun import freeze_time

from odoo import fields
from odoo.tests import common


@freeze_time("1980-01-01")
class TestProject(common.TransactionCase):
    def test_compute_current_sprint(self):
        # create a project and assign 3 sprints
        # should get as the current sprint the 1st one
        # (wich contains the current date inside start date and end date)

        project = self.env["project.project"].create(
            {
                "name": "test_project_scrum",
                "use_scrum": True,
            }
        )
        sprint1 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today(),
                "end_date": fields.date.today() + datetime.timedelta(days=7),
            }
        )
        sprint2 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=8),
                "end_date": fields.date.today() + datetime.timedelta(days=15),
            }
        )
        sprint3 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=16),
                "end_date": fields.date.today() + datetime.timedelta(days=23),
            }
        )
        sprint1.flush()
        sprint2.flush()
        sprint3.flush()
        project.flush()

        self.assertEqual(sprint1, project.current_sprint, "Wrong current sprint")

    def test_compute_next_sprint(self):
        # create a project and assign 3 sprints
        # should get as the next sprint the 2st one
        # (wich is the next one to the current sprint)

        project = self.env["project.project"].create(
            {
                "name": "test_project_scrum",
                "use_scrum": True,
            }
        )
        sprint1 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today(),
                "end_date": fields.date.today() + datetime.timedelta(days=7),
            }
        )
        sprint2 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=8),
                "end_date": fields.date.today() + datetime.timedelta(days=15),
            }
        )
        sprint3 = self.env["project.scrum.sprint"].create(
            {
                "project_id": project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=16),
                "end_date": fields.date.today() + datetime.timedelta(days=23),
            }
        )
        sprint1.flush()
        sprint2.flush()
        sprint3.flush()
        project.flush()

        self.assertEqual(sprint2, project.next_sprint, "Wrong next sprint")
