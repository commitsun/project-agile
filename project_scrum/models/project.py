from odoo import api, fields, models


class ProjectScrum(models.Model):
    _inherit = "project.project"
    use_scrum = fields.Boolean(default=False)
    scrum_team_id = fields.Many2one("project.scrum.team", string="Team")
    sprint_duration = fields.Integer(string="Sprint weeks")
    sprint_ids = fields.One2many("project.scrum.sprint", "project_id")
    scrum_sequence_id = fields.Many2one("ir.sequence")

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

    sprint_count = fields.Integer(
        compute="_compute_sprint_count", string="Sprint count"
    )

    def _compute_sprint_count(self):
        for project in self:
            project.sprint_count = self.env["project.scrum.sprint"].search_count(
                [("project_id", "=", project.id)]
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

    # ORM Overrides
    @api.model
    def create(self, vals):
        result = super(ProjectScrum, self).create(vals)
        if result["use_scrum"]:
            result["scrum_sequence_id"] = self.env["ir.sequence"].create(
                {
                    "name": "sequence for project: " + result["name"],
                    "code": "project.scrum." + str(result.id),
                    "padding": 3,
                    "prefix": result["name"] + "-sprint-",
                }
            )
        return result

    def write(self, vals):
        result = super(ProjectScrum, self).write(vals)
        if vals.get("use_scrum"):
            for project in self:
                if not project.scrum_sequence_id:
                    project.scrum_sequence_id = self.env["ir.sequence"].create(
                        {
                            "name": "sequence for project: " + project.name,
                            "code": "project.scrum." + str(project.id),
                            "padding": 3,
                            "prefix": project.name + "-sprint-",
                        }
                    )
        return result

    def unlink(self):
        project_ids = self._ids
        result = super(ProjectScrum, self).unlink()
        for project_id in project_ids:
            self.env["ir.sequence"].search(
                [("code", "=", "project.scrum." + str(project_id))]
            ).unlink()

        return result
