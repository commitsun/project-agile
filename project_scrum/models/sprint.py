from odoo import api, fields, models


class SprintScrum(models.Model):

    _name = "project.scrum.sprint"
    _description = "Sprints in the project"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        ondelete="cascade",
        required=True,
    )
    name = fields.Char(
        string="Name of the sprint",
        compute="_compute_sprint_name",
        store=True,
        readonly=False,
    )

    @api.depends("project_id")
    def _compute_sprint_name(self):
        for record in self:
            if record.project_id and not record.name:
                project_seq = self.env["ir.sequence"].next_by_code(
                    "project.scrum." + str(record.project_id.id)
                )
                if project_seq:
                    record.name = record.project_id.name + "-sprint-" + str(project_seq)

    start_date = fields.Date(string="Sprint start date")
    end_date = fields.Date(string="Sprint end date")
