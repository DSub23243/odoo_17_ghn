from odoo import api, fields, models, _
import requests


class ResCountry(models.Model):
    _inherit = 'res.country'

    district_id = fields.One2many(comodel_name='res.district', inverse_name='country_id', string="District", domain="")