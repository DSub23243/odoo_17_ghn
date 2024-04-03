from odoo import fields, models, api


class ModelName(models.Model):
    _inherits = 'learn_modern'

    code = fields.Char(string="code1")
