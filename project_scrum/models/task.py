from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    difficulty = fields.Selection("_get_difficulty_values", default="00")

    use_scrum = fields.Boolean(related="project_id.use_scrum", readonly=True)

    who = fields.Char(string="Who")
    what = fields.Char(string="What")
    why = fields.Char(string="Why")

    scrum_team_id = fields.Many2one("project.scrum.team", string="Team")

    def_of_done = fields.Html()
    technical_details = fields.Html()
    pr_link = fields.Char(string="Pull request link")

    scrum_allowed_users = fields.One2many("res.users", compute="_compute_allowed_users")
    scrum_users_domain = fields.Many2many(
        "res.users",
        compute="_compute_scrum_users_domain",
    )
    sprint_id = fields.Many2one(
        "project.scrum.sprint",
        string="Sprint",
        compute="_compute_sprint_id",
        readonly=False,
        store=True,
    )

    def _compute_allowed_users(self):
        for record in self:
            record.scrum_allowed_users = record.project_id.scrum_team_id.user_ids

    def _compute_scrum_users_domain(self):
        for record in self:
            if not record.use_scrum:
                record.scrum_users_domain = (
                    self.env["res.users"].search([("share", "=", False)]).mapped("id")
                )
            else:
                record.scrum_users_domain = (
                    self.env["res.users"]
                    .search(
                        [
                            ("share", "=", False),
                            ("id", "in", record.scrum_allowed_users.mapped("id")),
                        ]
                    )
                    .mapped("id")
                )

    @api.depends("stage_id")
    def _compute_sprint_id(self):
        for record in self:
            if record.stage_id.used_in_sprint:
                if (
                    record.sprint_id
                    and record.sprint_id != record.project_id.current_sprint
                ):
                    raise ValidationError(_("The task has already a sprint"))
                record.sprint_id = record.project_id.current_sprint
                record.date_deadline = record.project_id.current_sprint.end_date
