from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class CustomRateShipment(WebsiteSale):
    @http.route('/shop/carrier_rate_shipment', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def cart_carrier_rate_shipment(self, carrier_id, **kw):
        all_services = request.env['delivery.carrier'].search([('id', '=', carrier_id)])
        for carrier in all_services:
            if carrier.delivery_type == "ghn_shipping":
                return {'status': True, 'error_message': 'Custom rate calculation for carrier 4.'}
            else:
                return super(CustomRateShipment, self).cart_carrier_rate_shipment(carrier_id, **kw)