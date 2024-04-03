from odoo import _,fields, models, api, tools, SUPERUSER_ID
from datetime import date
from odoo.exceptions import UserError
from odoo.fields import Command
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # diary_order_ids = fields.One2many('diary.order', 'sale_order_id', string='Diary Orders')

    corresponding_diary_order_ids = fields.Many2many(
        comodel_name='diary.order',
        string="Diary Orders",
        store=True
    )

    def action_open_diary_order(self):
        self.ensure_one()
        diary_order = self.env['diary.order'].search([('order_code', '=', self.name)], limit=1)
        if not diary_order:
            raise UserError(_("No corresponding diary order found."))
        return {
            'name': 'Diary Orders',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'diary.order',
            'res_id': diary_order.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.model
    def _create_invoices(self, grouped=False, final=False):
        res = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)
        order_logs = []
        for order in self:
            product_ids = order.order_line.mapped('product_id')
            # Thêm kiểm tra để đảm bảo currency_id có giá trị
            if not order.currency_id:
                raise UserError(_("Order %s does not have a currency set.") % order.name)
            order_log_vals = {
                'name': order.partner_id.name,
                'order_code': order.name,
                'c_email': order.partner_id.email,
                'c_phone': order.partner_id.phone,
                'c_mobile': order.partner_id.mobile,
                'amount_total': order.amount_total,
                'currency_id': order.currency_id.id,
                'invoice_state': order.state,
                'user_id': order.user_id.id,
                'product_ids': [(6, 0, product_ids.ids)]
            }
            order_logs.append(order_log_vals)
        self.env['diary.order'].create(order_logs)
        return res

class ResPartner(models.Model):
    _inherit = 'res.partner'

    diary_order_ids = fields.One2many('diary.order', 'partner_id', string='Diary Orders')

class Product(models.Model):
    _inherit = 'product.product'

    diary_order_ids = fields.One2many('diary.order', 'product_ids', string='Diary Orders')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one('res.partner', string='Partner')

class Advance_payment(models.Model):
    _name = 'sales.advance.payment'
    _inherit = 'sale.advance.payment.inv'



class SaleOrderInvoice(models.Model):
    _inherit = 'sale.order'

    def action_view_related_invoices(self):
        self.ensure_one()
        action = self.env.ref('sales.action_view_order_invoices').read()[0]
        action['domain'] = [('partner_id', '=', self.partner_id.id)]
        action['context'] = {
            'default_partner_id': self.partner_id.id,
            'create': False,
        }
        action['target'] = 'new'
        action['view_mode'] = 'form'
        return action

class DiaryOrder(models.Model):
    _inherit = ['avatar.mixin', 'sale.advance.payment.inv', 'product.catalog.mixin', 'sale.advance.payment.inv']
    _name = 'diary.order'
    _description = 'Store purchase log including order code and customer information'

    amount_total = fields.Monetary(string='Total', readonly=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')
    currency_symbol = fields.Char(string="Currency Symbol", related="currency_id.symbol", readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    partner_id = fields.Many2one('res.partner', string="Partner")
    user_id = fields.Many2one('res.users', string="Salesperson")
    name = fields.Char(string="Customer", required=True, copy=False, readonly=False)
    order_code = fields.Char(string="Order Code", required=True, copy=False, readonly=True)
    product_ids = fields.Many2many('product.product', string='Products', readonly=True)
    invoice_status = fields.Selection([
        ('no', 'Invoice has been cancelled'),
        ('invoice', 'Invoice has been paid')
    ], string='Invoice Status', compute="_compute_invoice_status", store=True)
    invoice_state = fields.Char(string="Invoice state", copy=False)
    c_email = fields.Char(string="Email", readonly=True)
    c_phone = fields.Char(string="Phone", readonly=True, default="Empty phone number")
    c_mobile = fields.Char(string="Mobile", readonly=True, default="Empty mobile phone number")
    date = fields.Date(string="Invoice date", compute="_compute_date_new", store=True)
    order_line = fields.One2many('sale.order.line', 'order_id', string="Order Lines", auto_join=True)
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string="Pricelist",
        compute='_compute_pricelist_id',
        store=True,
        readonly=False,
        help="Pricelist used for this sale order.",

    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='sale_order_id.company_id',
        store=False,
        readonly=True)
    state = fields.Selection(related='sale_order_id.state', string="State", readonly=True)
    c_phone_template = fields.Char(string="Phone", compute="_compute_template_string", store=False)
    c_email_template = fields.Char(string="Email", compute="_compute_template_string", store=False)
    c_mobile_template = fields.Char(string="Mobile", compute="_compute_template_string", store=False)
    def _compute_template_string(self):
        for record in self:
            record.c_phone_template = "Data has not been added yet"
            record.c_email_template = "Data has not been added yet"
            record.c_mobile_template = "Data has not been added yet"
    @api.depends('sale_order_id')
    def _compute_pricelist_id(self):
        for order in self:
            if order.sale_order_id:
                order.pricelist_id = order.sale_order_id.pricelist_id
                print(order.pricelist_id)
            # print(order.sale_order_id.pricelist_id)

    @api.depends('order_code')
    def _compute_date_new(self):
        for rec in self:
            rec.date = date.today()

    @api.depends('name', 'c_email', 'amount_total', 'currency_symbol')
    def _compute_email_currency_formatted(self):
        for partner in self:
            emails_normalized = tools.email_normalize_all(partner.c_email)
            if emails_normalized:
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    ','.join(emails_normalized)
                )) + f' - {partner.currency_symbol} {partner.amount_total}'
            elif partner.c_email:
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    partner.c_email
                )) + f' - {partner.currency_symbol} {partner.amount_total}'
            else:
                partner.email_formatted = False

    @api.depends("invoice_state")
    def _compute_invoice_status(self):
        for order in self:
            if not order.invoice_state:
                order.invoice_status = "no"
            else:
                order.invoice_status = "invoice"

    @api.depends('name', 'partner_id.user_ids.share', 'partner_id.image_1920', 'partner_id.is_company',
                 'partner_id.type')
    def _compute_avatar_128(self):
        super()._compute_avatar_128()

    @api.depends('name', 'partner_id.user_ids.share', 'partner_id.image_1920', 'partner_id.is_company',
                 'partner_id.type')
    def _compute_avatar_1920(self):
        super()._compute_avatar_1920()

    # @api.model
    # def create_invoice_and_update_diary(self, order):
    #     generated_invoices = order._generate_downpayment_invoices()
    #     print('null ')
    #     for invoice in generated_invoices:
    #         diary_order_values = {
    #             'name': order.partner_id.name,
    #             'order_code': order.name,
    #             'c_email': order.partner_id.email,
    #             'c_phone': order.partner_id.phone or "Empty phone number",
    #             'c_mobile': order.partner_id.mobile or "Empty mobile phone number",
    #             'amount_total': order.amount_total,
    #             'currency_id': order.currency_id.id,
    #             'invoice_state': order.state,
    #             'user_id': order.user_id.id,
    #         }
    #         existing_diary_order = self.env['diary.order'].search([('sale_order_id', '=', order.id)])
    #         if existing_diary_order:
    #             existing_diary_order.write(diary_order_values)
    #         else:
    #             self.env['diary.order'].create(diary_order_values)
    #
    #     return generated_invoices

