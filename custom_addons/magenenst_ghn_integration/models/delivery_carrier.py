
from odoo import api, fields, models, _


class DeliveryCarrrier(models.Model):
    _inherit = 'delivery.carrier'

    service = fields.Selection([
        ('1', 'Express'),
        ('2', 'Standard'),
        ('4', 'Bulky and Heavy'),
    ], string='GHN Service', required=False, default='2',
        help="Choose your GHN shipping plan (Express, Standard or Bulky and Heavy)")


    delivery_type = fields.Selection(selection_add=[
        ('ghn_shipping', 'GHN Shipping')
    ], ondelete={'ghn_shipping': 'cascade'})

    def ghn_shipping_rate_shipment(self, order):
        carrier = self._match_address(order.partner_shipping_id)
        if not carrier:
            return {'success': False,
                    'price': 0.0,
                    'error_message': _('Error: this delivery method is not available for this address.'),
                    'warning_message': False}
        choose_delivery_carrier = self.env['choose.delivery.carrier'].create({
            'order_id': order.id,
            'carrier_id': self.id,
        })
        delivery_cost = choose_delivery_carrier.ghn_calculate_fee()
        price = delivery_cost['data']['total']
        return {'success': True,
                'price': price,
                'error_message': False,
                'warning_message': False}