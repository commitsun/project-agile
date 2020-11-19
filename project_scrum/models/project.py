from odoo import api, fields, models


class ProjectScrum(models.Model):
    _inherit = "project.project"
    use_scrum = fields.Boolean()
    team_id = fields.Many2one("project.scrum.team", string="Team")
    sprint_duration = fields.Integer(string="Sprint weeks")
    current_sprint = fields.Integer(string="Current sprint")
    next_sprint = fields.Date(string="Next sprint")
    sprint_ids = fields.One2many("project.scrum.sprint", "project_id")

    # ORM Overrides
    @api.model
    def create(self, vals):
        result = super(ProjectScrum, self).create(vals)
        self.env["ir.sequence"].create(
            {
                "name": "sequence for project " + result.name,
                "code": "project.scrum." + str(result.id),
                "prefix": "",
                "suffix": "",
                "padding": 3,
            }
        )

        return result
