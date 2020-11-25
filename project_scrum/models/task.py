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

    difficulty = fields.Selection("_get_difficulty_values")

    use_scrum = fields.Boolean(related="project_id.use_scrum", readonly=True)

    who = fields.Char(string="Who")
    what = fields.Char(string="What")
    why = fields.Char(string="Why")

    allowed_users = fields.Many2many(
        related="project_id.team_id.user_ids",
        readonly=True,
    )

    team_id = fields.Many2one(
        related="project_id.team_id",
        readonly=True,
    )

    def_of_done = fields.Html()
    technical_details = fields.Html()
    pr_link = fields.Char(string="Pull request link")

    sprint_id = fields.Many2one(
        "project.scrum.sprint",
        string="Sprint",
        compute="_compute_sprint_id",
        readonly=False,
        store="True",
    )

    @api.depends("stage_id")
    def _compute_sprint_id(self):
        for record in self:
            if record.stage_id.use_in_sprints:
                if (
                    record.sprint_id
                    and record.sprint_id != record.project_id.current_sprint
                ):
                    raise ValidationError(_("The task has already a sprint."))
                record.sprint_id = record.project_id.current_sprint
                record.date_deadline = record.project_id.current_sprint.end_date
