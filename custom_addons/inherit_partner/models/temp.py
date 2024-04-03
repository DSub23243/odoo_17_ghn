from odoo import fields, models, api


class temp(models.Model):
    _name = 'learn.temp'
    _description = 'Description'

    name = fields.Char()
