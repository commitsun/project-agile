from odoo import fields, models


class StageScrum(models.Model):
    _inherit = "project.task.type"
    used_in_sprint = fields.Boolean("Used in sprint")
