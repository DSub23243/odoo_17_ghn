from odoo import fields, models, api


class Modern_Inherit(models.Model):
    _inherit = 'learn.modern'

    code = fields.Char(string="Code", readonly=True)


    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('modern.seq')
        return super(Modern_Inherit, self).create(vals)