from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
        string="Sprint name",
        readonly=True,
        required=True,
        copy=False,
        default=lambda self: _("New"),
    )

    start_date = fields.Date(string="Sprint start date", required=True)
    end_date = fields.Date(string="Sprint end date", required=True)

    @api.constrains("start_date", "end_date")
    def check_dates(self):

        for record in self:
            if record.start_date < fields.date.today():
                raise ValidationError(
                    _("The start date cannot be earlier than current date")
                )

            elif record.end_date < fields.date.today():
                raise ValidationError(
                    _("The end date cannot be earlier than current date")
                )

            elif record.start_date >= record.end_date:
                raise ValidationError(
                    _("The end date cannot be earlier than start date")
                )

            for sprint in self.env["project.scrum.sprint"].search(
                [("project_id", "=", record.project_id.id), ("id", "!=", record.id)]
            ):
                # https://stackoverflow.com/questions/325933/determine-whether
                # -two-date-ranges-overlap/325964#325964

                # (StartA <= EndB)  and  (EndA >= StartB)
                if (
                    sprint.start_date <= record.end_date
                    and sprint.end_date >= record.start_date
                ):
                    raise ValidationError(_("Range of sprint overlaps another sprint"))

    @api.constrains("project_id")
    def check_is_scrum_project(self):
        for record in self:
            if not record.project_id.use_scrum:
                raise ValidationError(
                    _(
                        "Cannot create sprints belonging to projects"
                        " that do not use scrum"
                    )
                )

    @api.model
    def create(self, vals):
        result = super(SprintScrum, self).create(vals)
        if result["name"] == _("New"):
            result["name"] = result.project_id.scrum_sequence_id.next_by_id()
        return result
