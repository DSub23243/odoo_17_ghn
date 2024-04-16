from odoo import api, fields, models, _
import requests
import json

class ResDistrict(models.Model):
    _name = 'res.district'
    _description = 'District'
    _order = 'state_id'

    name = fields.Char("Name", required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'State', domain="[('country_id', '=', country_id)]")
    ghn_district_id = fields.Integer('GHN District ID', help='Mã quận/huyện theo Giao hàng Nhanh')

    def create_district_data(self):
        request_url = "https://dev-online-gateway.ghn.vn/shiip/public-api/master-data/district"
        ghn_token = self.env['ir.config_parameter'].sudo().get_param('ghn_token')
        headers = {
            'Content-type': 'application/json',
            'Token': ghn_token
        }
        req = requests.get(request_url, headers=headers)
        req.raise_for_status()
        content = req.json()
        print(content)
        data = content['data']
        for rec in data:
            existed_state = self.env['res.country.state'].sudo().search([('ghn_province_id', '=', rec['ProvinceID'])], limit=1)
            if existed_state:
                vals = {}
                vals['state_id'] = existed_state.id
                vals['country_id'] = existed_state.country_id.id
                vals['name'] = rec['DistrictName']
                vals['ghn_district_id'] = rec['DistrictID']
                self.env['res.district'].sudo().create(vals)

