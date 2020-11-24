from odoo import fields, models


class TeamScrum(models.Model):
    _name = "project.scrum.team"
    _description = "Scrum team"
    name = fields.Char(string="Name")

    user_ids = fields.Many2many(
        comodel_name="res.users",
        relation="team_scrum_user_rel",
        column1="team_id",
        column2="user_id",
        string="Users",
    )
