from odoo import api, fields, models, _
import requests
import json

class ResWard(models.Model):
    _name = 'res.ward'
    _description = 'Res Ward'
    _order = 'state_id'

    name = fields.Char("Name", required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', 'State', domain="[('country_id', '=', country_id)]")
    district_id = fields.Many2one('res.district', 'District', domain="[('state_id', '=', state_id)]")
    ghn_ward_id = fields.Char("GHN Ward Code", help='Mã phường/xã theo Giao hàng Nhanh')


    def create_ward_data(self):
        all_districts = self.env['res.district'].search([])
        request_url = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/ward"
        ghn_token = self.env['ir.config_parameter'].sudo().get_param('ghn_token')
        headers = {
            'Content-type': 'application/json',
            'Token': ghn_token
        }

        for district in all_districts:
            payload = {
                'district_id': district.ghn_district_id,
            }
            req = requests.get(request_url, params=payload, headers=headers)
            req.raise_for_status()
            content = req.json()
            if content and content.get('data'):
                ward_data = content['data']
                for rec in ward_data:
                    ward_vals = {
                        'name': rec['WardName'],
                        'country_id': district.country_id.id,
                        'state_id': district.state_id.id,
                        'district_id': district.id,
                        'ghn_ward_id': rec['WardCode']
                    }
                    existing_ward = self.env['res.ward'].search([
                        ('ghn_ward_id', '=', rec['WardCode']),
                        ('district_id', '=', district.id)
                    ], limit=1)
                    if not existing_ward:
                        self.env['res.ward'].create(ward_vals)
