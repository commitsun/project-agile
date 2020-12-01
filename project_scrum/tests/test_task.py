import datetime

from freezegun import freeze_time

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common


@freeze_time("1980-01-01")
class TestProject(common.TransactionCase):
    def create_common_scenario(self):
        self.project = self.env["project.project"].create(
            {
                "name": "test_project_scrum",
                "use_scrum": True,
            }
        )
        self.sprint1 = self.env["project.scrum.sprint"].create(
            {
                "project_id": self.project.id,
                "start_date": fields.date.today(),
                "end_date": fields.date.today() + datetime.timedelta(days=7),
            }
        )
        self.sprint2 = self.env["project.scrum.sprint"].create(
            {
                "project_id": self.project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=8),
                "end_date": fields.date.today() + datetime.timedelta(days=15),
            }
        )
        self.sprint3 = self.env["project.scrum.sprint"].create(
            {
                "project_id": self.project.id,
                "start_date": fields.date.today() + datetime.timedelta(days=16),
                "end_date": fields.date.today() + datetime.timedelta(days=23),
            }
        )
        self.no_sprint_stage = self.env["project.task.type"].create(
            {
                "name": "test task",
                "use_in_sprints": False,
            }
        )

        self.sprint_stage = self.env["project.task.type"].create(
            {
                "name": "test task",
                "use_in_sprints": True,
            }
        )

        self.task = self.env["project.task"].create(
            {
                "project_id": self.project.id,
                "name": "test task",
            }
        )

    def test_task_into_sprint_stage01(self):
        # move a task to a sprint stage
        # task gets deadline from sprint end date

        # ARRANGE
        self.create_common_scenario()

        # ACT
        self.task.stage_id = self.sprint_stage
        self.task.flush()

        # ASSERT
        self.assertEqual(
            self.task.date_deadline,
            self.sprint1.end_date,
            "The deadline is not correct",
        )

    def test_task_into_sprint_stage02(self):
        # move a task to a sprint stage
        # task gets current sprint according to the current date
        # (today between the start date and the end date of the sprint1)

        # ARRANGE
        self.create_common_scenario()

        # ACT
        self.task.stage_id = self.sprint_stage
        self.task.flush()

        # ASSERT
        self.assertEqual(self.task.sprint_id, self.sprint1, "The sprint is not correct")

    def test_task_into_sprint_stage03(self):
        # move a task to a sprint stage
        # task gets current sprint

        # ARRANGE
        self.create_common_scenario()

        # ACT
        self.task.stage_id = self.sprint_stage
        self.task.flush()

        # ASSERT
        self.assertEqual(
            self.task.sprint_id, self.sprint1, "Task asigned to incorrect sprint."
        )

    def test_task_into_sprint_stage04(self):
        # day 1 - move a task to a sprint stage
        # day 1 - move same task to a non sprint stage
        # day 2 - move same task to a sprint stage
        #   should raises validation error because
        #   the task has already a sprint

        freezer = freeze_time("1980-01-01")
        freezer.start()

        # ARRANGE
        self.create_common_scenario()
        self.task.stage_id = self.sprint_stage
        self.task.flush()
        self.task.stage_id = self.no_sprint_stage
        self.task.flush()

        freezer.stop()
        self.project.invalidate_cache()
        freezer = freeze_time("1980-01-11")
        freezer.start()

        # ACT & ASSERT
        with self.assertRaises(ValidationError):
            self.task.stage_id = self.sprint_stage
            self.task.flush()

        freezer.stop()
