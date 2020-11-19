from odoo import api, fields, models


class TaskScrum(models.Model):
    _inherit = "project.task"
    _order = "sequence"

    @api.model
    def _get_difficulty_values(self):
        return [
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("5", "5"),
            ("8", "8"),
            ("13", "13"),
            ("21", "21"),
            ("34", "34"),
            ("55", "55"),
            ("89", "89"),
            ("144", "144"),
            ("00", "Not Set"),
        ]

    difficulty = fields.Selection("_get_difficulty_values")

    use_scrum = fields.Boolean(
        compute="_compute_project_use_scrum", search="_search_project_use_scrum"
    )

    who = fields.Char(string="Who")
    what = fields.Char(string="What")
    why = fields.Char(string="Why")

    allowed_users = fields.One2many("res.users", compute="_compute_allowed_users")

    def_of_done = fields.Html()
    technical_details = fields.Html()
    pr_link = fields.Char(string="Pull request link")

    def _compute_allowed_users(self):
        for record in self:
            record.allowed_users = record.project_id.team_id.user_ids

    def _compute_project_use_scrum(self):
        for record in self:
            record.use_scrum = self.project_id.use_scrum
