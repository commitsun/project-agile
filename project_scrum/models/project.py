from odoo import api, fields, models


class ProjectScrum(models.Model):
    _inherit = "project.project"
    use_scrum = fields.Boolean()
    team_id = fields.Many2one("project.scrum.team", string="Team")
    sprint_duration = fields.Integer(string="Sprint weeks")
    sprint_ids = fields.One2many("project.scrum.sprint", "project_id")
    current_sprint = fields.Many2one(
        "project.scrum.sprint",
        string="Current sprint",
        compute="_compute_current_sprint",
        readonly=True,
        store=False,
    )
    next_sprint = fields.Many2one(
        "project.scrum.sprint",
        string="Next sprint",
        compute="_compute_next_sprint",
        readonly=True,
        store=False,
    )

    def _compute_current_sprint(self):
        for record in self.sorted(key=lambda r: r.id):
            record.current_sprint = False
            for sprint in record.sprint_ids.sorted(key=lambda r: r.start_date):
                if sprint.start_date <= fields.date.today() <= sprint.end_date:
                    record.current_sprint = sprint
                    break

    def _compute_next_sprint(self):
        for record in self.sorted(key=lambda r: r.id):
            record.next_sprint = False
            for sprint in record.sprint_ids.sorted(key=lambda r: r.start_date):
                if fields.date.today() < sprint.start_date:
                    record.next_sprint = sprint
                    break

    def project_sequence(self, project_id, project_name):
        project_seq = self.env["ir.sequence"].search(
            [("code", "=", "project.scrum." + str(project_id))]
        )
        if not project_seq:
            self.env["ir.sequence"].create(
                {
                    "name": "sequence for project: " + project_name,
                    "code": "project.scrum." + str(project_id),
                    "padding": 3,
                }
            )

    # ORM Overrides
    def write(self, vals):
        result = super(ProjectScrum, self).write(vals)
        if vals.get("use_scrum"):
            for project in self:
                self.project_sequence(project.id, project.name)
        return result

    @api.model
    def create(self, vals):
        result = super(ProjectScrum, self).create(vals)
        if vals.get("use_scrum"):
            for project in result:
                self.project_sequence(project.id, project.name)
        return result

    def unlink(self):
        project_ids = self._ids

        result = super(ProjectScrum, self).unlink()
        for project_id in project_ids:
            self.env["ir.sequence"].search(
                [("code", "=", "project.scrum." + str(project_id))]
            ).unlink()

        return result
