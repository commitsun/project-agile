from odoo import api, fields, models


class ProjectScrum(models.Model):
    _inherit = "project.project"
    use_scrum = fields.Boolean()
    team_id = fields.Many2one("project.scrum.team", string="Team")
    sprint_duration = fields.Integer(string="Sprint weeks")
    sprint_ids = fields.One2many("project.scrum.sprint", "project_id")

    current_sprint = fields.Many2one(
        "project.scrum.sprint",
        string="The current sprint",
        compute="_compute_current_sprint",
        readonly=True,
    )

    next_sprint = fields.Many2one(
        "project.scrum.sprint",
        string="The next sprint",
        compute="_compute_next_sprint",
        readonly=True,
    )

    @api.depends("sprint_ids")
    def _compute_current_sprint(self):
        for record in self.sorted(
            key=lambda r: r.id
        ):  # <-- REVIEW (order by id/sequence)
            record.current_sprint = False
            for sprint in record.sprint_ids.sorted(key=lambda r: r.start_date):
                if sprint.start_date <= fields.date.today() <= sprint.end_date:
                    record.current_sprint = sprint
                    break

    @api.depends("sprint_ids")
    def _compute_next_sprint(self):
        for record in self.sorted(
            key=lambda r: r.id
        ):  # <-- REVIEW (order by id/sequence)
            record.next_sprint = False
            for sprint in record.sprint_ids.sorted(key=lambda r: r.start_date):
                if fields.date.today() < sprint.start_date:
                    record.next_sprint = sprint
                    break

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
