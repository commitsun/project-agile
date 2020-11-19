from odoo import fields, models


class StageScrum(models.Model):
    _inherit = "project.task.type"

    use_in_sprints = fields.Boolean("Use in sprints")
