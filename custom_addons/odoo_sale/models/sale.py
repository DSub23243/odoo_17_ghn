from odoo import models, fields, api

class sale(models.Model):
    _name = "learn.sale"
    _description = "sale tutorial"

    name = fields.Char()
    price = fields.Integer()
    cost = fields.Integer()
    description = fields.Text()
    active = fields.Boolean()
