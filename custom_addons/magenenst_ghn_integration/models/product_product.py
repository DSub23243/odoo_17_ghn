from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.template'

    length = fields.Integer(
        string='Chiều dài (cm)',
        default=1,
        help='Là khối lượng được tính dựa theo công thức (DxRxC/5000)'
    )
    width = fields.Integer(
        string='Chiều rộng (cm)',
        default=1,
        help='Là khối lượng được tính dựa theo công thức (DxRxC/5000)'
    )
    height = fields.Integer(
        string='Chiều cao (cm)',
        default=1,
        help='Là khối lượng được tính dựa theo công thức (DxRxC/5000)'
    )
