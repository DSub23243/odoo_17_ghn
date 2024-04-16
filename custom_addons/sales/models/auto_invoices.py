from odoo import fields, models, api
# from payment_demo import PaymentTransaction


class AutoInvoices(models.Model):
    _inherit = 'sale.order'

    # Thêm phương thức tạo hóa đơn tự động
    def action_auto_invoice(self):
        # Tạo hóa đơn
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [(0, 0, {
            'name': line.product_id.name,
            'quantity': line.product_uom_qty,
            'price_unit': line.price_unit,
            'tax_ids': [(6, 0, line.tax_id.ids)],
            'product_id': line.product_id.id,
            }) for line in self.order_line],
        })

        if self.invoice_status == "no":
            self.write({'invoice_status': 'to invoice', 'state': 'sale'})
            if self.invoice_status == 'to invoice':
                self._create_invoices()
                invoice.action_post()

        return True