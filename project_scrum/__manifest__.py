{
    "name": "Project Scrum",
    "summary": "Use Scrum Method to manage your project",
    "version": "14.0.1.0.1",
    "category": "Project Management",
    "author": "CommitSun, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/project-agile",
    "installable": True,
    "application": True,
    "license": "AGPL-3",
    "depends": [
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project.xml",
        "views/team.xml",
        "views/task.xml",
        "views/sprint.xml",
        "views/stage.xml",
    ],
}
