from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'
    use_scrum = fields.Boolean()

    manhours = fields.Integer(
        string='Man Hours',
        help="How many hours you expect this project "
        "needs before it's finished"
    )
