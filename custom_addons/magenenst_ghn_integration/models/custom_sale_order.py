from odoo import models, api


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    def _check_carrier_quotation(self, force_carrier_id=None, keep_carrier=False):
        self.ensure_one()
        DeliveryCarrier = self.env['delivery.carrier']
        if self.only_services:
            self._remove_delivery_line()
            return True
        else:
            self = self.with_company(self.company_id)
            # attempt to use partner's preferred carrier
            if not force_carrier_id and self.partner_shipping_id.property_delivery_carrier_id and not keep_carrier:
                force_carrier_id = self.partner_shipping_id.property_delivery_carrier_id.id
                carrier = force_carrier_id and DeliveryCarrier.browse(force_carrier_id) or self.carrier_id
                available_carriers = self._get_delivery_methods()
                if carrier:
                    if carrier not in available_carriers:
                        carrier = DeliveryCarrier
                    else:
                        # set the forced carrier at the beginning of the list to be verfied first below
                        available_carriers -= carrier
                        available_carriers = carrier + available_carriers
                if force_carrier_id or not carrier or carrier not in available_carriers:
                    for delivery in available_carriers:
                        verified_carrier = delivery._match_address(self.partner_shipping_id)
                        if verified_carrier:
                            carrier = delivery
                            break
                    self.write({'carrier_id': carrier.id})
                self._remove_delivery_line()

                all_services = self.env['delivery.carrier'].search([('id', '=', carrier.id)])
                for carrier in all_services:
                    if carrier.delivery_type != "ghn_shipping":
                        res = carrier.rate_shipment(self)
                        if res.get('success'):
                            self.set_delivery_line(carrier, res['price'])
                            self.delivery_rating_success = True
                            self.delivery_message = res['warning_message']
                        else:
                            self.set_delivery_line(carrier, 0.0)
                            self.delivery_rating_success = False
                            self.delivery_message = res['error_message']
                    else:
                        choose_delivery_carrier_wizard = self.env['choose.delivery.carrier'].create({
                            'order_id': self.id,
                            'carrier_id': carrier.id,
                        })
                        delivery_cost = choose_delivery_carrier_wizard.ghn_calculate_fee()
                        print("oke")

                        total_fee = delivery_cost['data']['total']
                        self.set_delivery_line(carrier, total_fee)
                return bool(carrier)
            result = super(CustomSaleOrder, self)._check_carrier_quotation(force_carrier_id, keep_carrier)
            return result