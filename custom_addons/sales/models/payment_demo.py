from odoo import _,models, fields, api
import logging
from odoo.exceptions import  UserError, ValidationError

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'
    _description = 'Payment Provider'

    active_automatic_invoicing = fields.Boolean(
        string="Active Automatic Invoicing",
        default=True,
        help="Check this to enable automatic invoicing and notifications after payment."
    )
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    provider_id = fields.Many2one('payment.provider', string="Payment Provider")
    # kiểm tra và tạo hóa đơn
    def _handle_post_payment_processing(self, sale_order):
        _logger.info("Handling post-payment processing for sale order %s", sale_order.name)
        if sale_order.state == 'sale' and sale_order.invoice_status == 'to invoice':
            invoice = sale_order._create_invoices()
            _logger.info("Invoice created: %s", invoice)
            if invoice:
                invoice.action_post()

                diary_order = self.env['diary.order'].search([('order_code', '=', sale_order.name)], limit=1)
                if diary_order:
                    diary_order.write({
                        'currency_id': sale_order.currency_id.id,
                    })
                else:
                    diary_order_vals = {
                        'order_code': sale_order.name,
                        'currency_id': sale_order.currency_id.id,
                    }
                    diary_order = self.env['diary.order'].create(diary_order_vals)

                related_sale_order = self.env['sale.order'].search([('transaction_ids', 'in', self.id)], limit=1)
                template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
                template_order = self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)
                if template:
                    template.send_mail(invoice.id, force_send=True, )
                    template_order.send_mail(related_sale_order.id, force_send=True)
                    _logger.info("Email hóa đơn đã được gửi cho %s", invoice.partner_id.name)
                else:
                    _logger.error("Không tìm thấy mẫu email để gửi hóa đơn.")

            else:
                _logger.warning("Không tạo được hóa đơn cho đơn bán hàng %s", sale_order.name)
        else:
            _logger.info("Đơn hàng %s không đúng trạng thái hoặc trạng thái hóa đơn để tạo hóa đơn",
                         sale_order.name)

    # Tìm kiếm Transaction_ids trong sale.order
    def write(self, vals):
        res = super(PaymentTransaction, self).write(vals)
        for transaction in self:
            sale_order = self.env['sale.order'].search([('transaction_ids', 'in', transaction.id)], limit=1)
            if sale_order:
                provider = self.provider_id
                if provider and not provider.active_automatic_invoicing:
                    _logger.info("Automatic invoicing is disable for orders %s", provider.name)
                    return
                transaction._handle_post_payment_processing(sale_order)
        return res

    # def _process_notification_data(self, notification_data):
    #     super()._process_notification_data(notification_data)
    #     if self.provider_code != 'demo' or self.state != 'done':
    #         return
    #     self.env['sale.order'].create_quotations_from_demo_provider()

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    transaction_ids = fields.Many2many('payment.transaction', string='Transactions')



    # Duyệt và chuyển trạng thái các đơn hàng trong sale.order
    def create_quotations_from_demo_provider(self):
        print("Các đơn hàng đủ điều kiện...")
        orders_to_invoice = self.search([
            ('invoice_status', '=', 'to invoice'),
            ('state', '=', 'sale'),
            ('transaction_ids.provider_code', '=', 'demo'),
            ('transaction_ids.state', '=', 'done')
        ])
        if orders_to_invoice:
            print("Các đơn hàng tìm thấy:", orders_to_invoice)
        else:
            print("Không tìm thấy điều kiện")

        for order in orders_to_invoice:
            print("Xử lý đơn hàng:", order.name)
            invoice = order._create_invoices()
            order.invoice_status = 'invoiced'
            if not invoice:
                raise UserError(_("Invoice could not be created for order %s") % order.name)
            invoice.action_post()

