from odoo import fields, models


class UserScrum(models.Model):
    _inherit = "res.users"

    scrum_team_ids = fields.Many2many(
        comodel_name="project.scrum.team",
        relation="team_scrum_user_rel",
        column1="user_id",
        column2="scrum_team_id",
        string="Teams",
    )
