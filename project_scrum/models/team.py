from odoo import models, fields

class TeamScrum(models.Model):
    _name = "project.scrum.team"
    _description = "Scrum team"
    name = fields.Char(
        string ="Name"
    )

    user_ids = fields.Many2many(
        "res.users",
        "id",
        string="Users"
    )
