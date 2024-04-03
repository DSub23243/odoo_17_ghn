from odoo import fields, models, api


class Calculate(models.Model):
    _inherit = "res.partner"

    limit_credit = fields.Float(string="limit Credit")