from odoo import fields, models, api


class Modern_Inherit(models.Model):
    _inherits = "learn.modern"
    _name = 'ProjectName.TableName'
    _description = 'Description'

    name = fields.Char()
