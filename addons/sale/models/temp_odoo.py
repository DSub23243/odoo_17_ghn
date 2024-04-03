from odoo import fields, models, api


class temp_odoo(models.Model):
    _name = 'temp.odoo'
    _description = 'Description'

    name = fields.Char()
