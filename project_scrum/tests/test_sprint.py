import datetime

from freezegun import freeze_time

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common


@freeze_time("1980-01-01")
class TestSprint(common.TransactionCase):
    def create_common_scenario(self):
        # create a project with scrum = True
        self.project_test = self.env["project.project"].create(
            {
                "name": "test_project_scrum",
                "use_scrum": True,
            }
        )

    def test_wrong_dates(self):
        # ARRANGE
        self.create_common_scenario()
        dates = [
            {
                "start_date": fields.date.today() + datetime.timedelta(days=-1),
                "end_date": fields.date.today() + datetime.timedelta(days=1),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=1),
                "end_date": fields.date.today() + datetime.timedelta(days=-1),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=2),
                "end_date": fields.date.today() + datetime.timedelta(days=1),
            },
        ]
        # ACT & ASSERTS
        for i in dates:
            with self.subTest(i=i):
                with self.assertRaises(ValidationError):
                    self.env["project.scrum.sprint"].create(
                        {
                            "project_id": self.project_test.id,
                            "start_date": i["start_date"],
                            "end_date": i["end_date"],
                        }
                    )

    def test_range_sprint_overlaps(self):

        self.create_common_scenario()

        self.env["project.scrum.sprint"].create(
            {
                "project_id": self.project_test.id,
                "start_date": fields.date.today() + datetime.timedelta(days=1),
                "end_date": fields.date.today() + datetime.timedelta(days=4),
            }
        ).flush()

        #    +=======+=======+=======+=======+=======+=======+=======+
        #    |sprint | day 0 | day 1 | day 2 | day 3 | day 4 | day 5 |
        #    +=======+=======+=======+=======+=======+=======+=======+
        #    | sp_1  |       |   <---|-------|-------|-->    |       |
        #    | tst1  |       |   <---|-------|-------|-->    |       |
        #    | tst2  |       |       |   <---|--->   |       |       |
        #    | tst3  |       |   <---|-------|--->   |       |       |
        #    | tst4  |       |       |   <---|-------|-->    |       |
        #    | tst5  |   <---|-------|--->   |       |       |       |
        #    | tst6  |       |       |   <---|-------|-------|--->   |
        #    | tst7  |   <---|-------|-------|-------|-------|--->   |
        #    +=======+=======+=======+=======+=======+=======+=======+

        dates = [
            {
                "start_date": fields.date.today() + datetime.timedelta(days=1),
                "end_date": fields.date.today() + datetime.timedelta(days=4),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=2),
                "end_date": fields.date.today() + datetime.timedelta(days=3),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=1),
                "end_date": fields.date.today() + datetime.timedelta(days=3),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=2),
                "end_date": fields.date.today() + datetime.timedelta(days=4),
            },
            {
                "start_date": fields.date.today(),
                "end_date": fields.date.today() + datetime.timedelta(days=2),
            },
            {
                "start_date": fields.date.today() + datetime.timedelta(days=2),
                "end_date": fields.date.today() + datetime.timedelta(days=5),
            },
            {
                "start_date": fields.date.today(),
                "end_date": fields.date.today() + datetime.timedelta(days=5),
            },
        ]

        # ACT & ASSERTS
        for i in dates:
            with self.subTest(i=i):
                with self.assertRaises(ValidationError):
                    self.env["project.scrum.sprint"].create(
                        {
                            "project_id": self.project_test.id,
                            "start_date": i["start_date"],
                            "end_date": i["end_date"],
                        }
                    )

    def test_create_from_no_scrum_project(self):
        # create a project with scrum = True
        project_no_scrum = self.env["project.project"].create(
            {
                "name": "test_project_scrum",
                "use_scrum": False,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["project.scrum.sprint"].create(
                {
                    "project_id": project_no_scrum.id,
                }
            )
